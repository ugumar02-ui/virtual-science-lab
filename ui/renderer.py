"""Generic, schema-driven practical renderer."""

import streamlit as st
import plotly.graph_objects as go

from core import registry


def _build_controls(practical: dict, teacher_mode: bool) -> dict:
    controls = practical.get("controls", [])
    params: dict = {}
    visible = []
    for ctrl in controls:
        if ctrl.get("teacher_only") and not teacher_mode:
            params[ctrl["key"]] = ctrl["default"]
        else:
            visible.append(ctrl)

    params.update(practical.get("fixed", {}))

    if not visible:
        return params

    cols = st.columns(min(3, len(visible)))
    for i, ctrl in enumerate(visible):
        unit = ctrl.get("unit", "")
        label = f"{ctrl['label']} ({unit})" if unit else ctrl["label"]
        key = f"{practical['id']}::{ctrl['key']}"
        with cols[i % len(cols)]:
            if ctrl["type"] == "slider":
                params[ctrl["key"]] = st.slider(
                    label,
                    min_value=float(ctrl["min"]),
                    max_value=float(ctrl["max"]),
                    value=float(ctrl["default"]),
                    step=float(ctrl["step"]),
                    key=key,
                    help=ctrl.get("help"),
                )
            elif ctrl["type"] == "select":
                options = ctrl["options"]
                params[ctrl["key"]] = st.selectbox(
                    label,
                    options=options,
                    index=options.index(ctrl["default"]),
                    key=key,
                    help=ctrl.get("help"),
                )
            elif ctrl["type"] == "number":
                params[ctrl["key"]] = st.number_input(
                    label,
                    min_value=float(ctrl["min"]),
                    max_value=float(ctrl["max"]),
                    value=float(ctrl["default"]),
                    step=float(ctrl["step"]),
                    key=key,
                    help=ctrl.get("help"),
                )
            else:
                raise ValueError(f"Unknown control type: {ctrl['type']!r}")
    return params


def _plot(result: dict) -> None:
    series = result.get("series") or []
    if not series:
        return
    fig = go.Figure()
    for s in series:
        if s.get("type") == "bar":
            fig.add_trace(go.Bar(x=s["x"], y=s["y"], name=s["name"], opacity=0.85))
            continue
        fig.add_trace(
            go.Scatter(
                x=s["x"],
                y=s["y"],
                name=s["name"],
                mode=s.get("mode", "lines"),
                line=dict(width=3),
                marker=dict(size=9),
            )
        )
    fig.update_layout(
        xaxis_title=result.get("x_label", ""),
        yaxis_title=result.get("y_label", ""),
        template="plotly_white",
        height=400,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch")


def _swatch(colour: str, label: str) -> None:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:14px;margin:6px 0 14px 0">
          <div style="width:90px;height:60px;border-radius:12px;background:{colour};
                      border:1px solid rgba(0,0,0,.15)"></div>
          <div style="font-size:1.05rem"><b>Observation:</b> {label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _report(practical: dict, result: dict, error: float | None) -> str:
    q = practical.get("quantity")
    lines = [
        f"# {practical['title']}",
        "",
        f"*{practical.get('subtitle', '')}*  ",
        f"Class {practical.get('grade', '')} · AKU-EB practical",
        "",
        "## Apparatus",
        *[f"- {a}" for a in practical.get("apparatus", [])],
        "",
        "## Theory",
        practical.get("theory", ""),
        "",
        "## Procedure",
        *[f"{i}. {s}" for i, s in enumerate(practical.get("procedure", []), 1)],
        "",
        "## Observations",
    ]
    if result.get("table"):
        cols = list(result["table"][0].keys())
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join(["---"] * len(cols)) + "|")
        for row in result["table"]:
            lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")

    lines.append("")
    lines.append("## Result")
    if q:
        d = q.get("decimals", 2)
        lines += [
            f"- {q['label']}: **{result['measured']:.{d}f} {q.get('unit', '')}**",
            f"- Accepted value: {result['accepted']:.{d}f} {q.get('unit', '')}",
            f"- Percentage error: {error:.2f} %",
        ]
    elif result.get("observation"):
        obs = result["observation"]
        lines.append(f"- {obs['label']}: **{obs['value']}**")

    for note in result.get("notes", []):
        lines += ["", f"> {note}"]

    lines += [
        "",
        "## Precautions",
        "- Read all instruments at eye level to avoid parallax error.",
        "- Repeat readings and take a mean.",
        "- Record readings to the correct number of decimal places.",
    ]
    return "\n".join(lines)


def render(practical: dict) -> None:
    from content import level_of

    st.title(practical["title"])
    st.caption(
        f"{practical.get('subtitle', '')}  ·  Class {practical['grade']} "
        f"({level_of(practical['grade'])}) · AKU-EB"
    )

    tab_sim, tab_theory, tab_viva = st.tabs(
        ["🔬 Simulation", "📖 Theory & Procedure", "🎓 Viva"]
    )

    with tab_theory:
        st.subheader("Theory")
        st.markdown(practical.get("theory", ""))
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Apparatus")
            for item in practical.get("apparatus", []):
                st.markdown(f"- {item}")
        with c2:
            st.subheader("Procedure")
            for i, step in enumerate(practical.get("procedure", []), 1):
                st.markdown(f"{i}. {step}")

    with tab_viva:
        st.subheader("Viva questions")
        for i, qa in enumerate(practical.get("viva", []), 1):
            with st.expander(f"Q{i}. {qa['q']}"):
                st.markdown(qa["a"])

    with tab_sim:
        teacher_mode = st.session_state.get("teacher_mode", False)
        st.subheader("Set up the apparatus")
        params = _build_controls(practical, teacher_mode)

        if "seed" not in st.session_state:
            st.session_state.seed = 1

        left, right = st.columns([1, 3])
        with left:
            if st.button("🔄 New set of readings", width="stretch"):
                st.session_state.seed += 1
            st.caption(f"Trial run #{st.session_state.seed}")
        with right:
            if teacher_mode:
                st.info("Teacher mode: instructor-only values are visible below.")

        student_titre = None
        if practical.get("canvas") == "titration":
            from ui import canvas as canvas_ui

            st.subheader("Perform the titration")
            st.caption(
                "Open the tap, keep the flask swirling, and close it the moment a pale pink "
                "colour persists. Add one drop at a time near the end."
            )
            canvas_ui.titration_canvas(
                acid_conc=params["acid_conc"],
                acid_volume=params["acid_volume"],
                base_conc=params["base_conc"],
                n_factor=params.get("n_factor", 1),
                initial_reading=st.session_state.get(f"{practical['id']}::initial", 0.0),
            )
            with st.container(border=True):
                st.markdown("**Record your own reading**")
                c1, c2 = st.columns([2, 1])
                student_titre = c1.number_input(
                    "Mean titre of base used (cm³)",
                    min_value=0.0,
                    max_value=50.0,
                    value=0.0,
                    step=0.05,
                    key=f"{practical['id']}::titre",
                    help="Final burette reading minus initial reading, averaged over concordant runs.",
                )
                c2.metric("Your titre", f"{student_titre:.2f} cm³")
                if student_titre == 0:
                    st.caption(
                        "Run the titration above, then type the volume you used to have the "
                        "app calculate the concentration from *your* reading."
                    )

        engine = registry.get_engine(practical["engine"])
        result = engine(**params, seed=st.session_state.seed)

        if student_titre:
            n = params.get("n_factor", 1)
            measured = params["base_conc"] * student_titre / (n * params["acid_volume"])
            result["measured"] = measured
            result["accepted"] = params["acid_conc"]
            result["table"] = [
                {
                    "Mean titre (cm³)": round(student_titre, 2),
                    "Moles of base used (mol)": round(
                        params["base_conc"] * student_titre / 1000, 6
                    ),
                    "Calculated concentration (mol/dm³)": round(measured, 4),
                }
            ]
            result["notes"] = [
                f"Calculated from your own reading: c(acid) = c(base) × V(base) ÷ "
                f"({n} × V(acid)) = {params['base_conc']:.2f} × {student_titre:.2f} ÷ "
                f"({n} × {params['acid_volume']:.0f}) = {measured:.4f} mol/dm³."
            ] + result["notes"]

        st.divider()
        q = practical.get("quantity")
        error = None
        if q and result.get("kind") == "quantitative":
            measured = result["measured"]
            accepted = result["accepted"]
            error = abs(measured - accepted) / abs(accepted) * 100 if accepted else 0.0
            d = q.get("decimals", 2)

            m1, m2, m3 = st.columns(3)
            m1.metric(q["label"], f"{measured:.{d}f} {q.get('unit', '')}".strip())
            m2.metric("Accepted value", f"{accepted:.{d}f} {q.get('unit', '')}".strip())
            m3.metric("Percentage error", f"{error:.2f} %")

            if error <= q["tolerance"] * 100:
                st.success(
                    f"Within experimental error ({error:.2f} % ≤ "
                    f"{q['tolerance'] * 100:.0f} %). Result accepted."
                )
            else:
                st.error(
                    f"Outside experimental error ({error:.2f} % > "
                    f"{q['tolerance'] * 100:.0f} %). Check your procedure and repeat."
                )
        elif result.get("observation"):
            obs = result["observation"]
            st.metric(obs["label"], obs["value"])
            _swatch(obs["colour"], obs["value"])

        if result.get("observation") and result.get("kind") == "quantitative":
            obs = result["observation"]
            _swatch(obs["colour"], obs["value"])

        _plot(result)

        if result.get("extras"):
            extras = result["extras"]
            cols = st.columns(len(extras))
            for col, (label, value, unit) in zip(cols, extras):
                col.metric(label, f"{value} {unit}".strip())

        if result.get("table"):
            st.subheader("Observation table")
            st.dataframe(result["table"], width="stretch", hide_index=True)

        for note in result.get("notes", []):
            st.info(note)

        st.download_button(
            "⬇️ Download lab report (.md)",
            data=_report(practical, result, error),
            file_name=f"{practical['id']}-report.md",
            mime="text/markdown",
        )
