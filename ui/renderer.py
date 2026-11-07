"""Generic, schema-driven practical renderer.

One function renders every practical in the catalogue: controls come from the
practical schema, the measurement comes from its engine, and the surrounding
teaching material comes from the attached ``depth`` record.
"""

from __future__ import annotations

import random

import plotly.graph_objects as go
import streamlit as st

from core import registry
from ui import bench, theme

PALETTE = ["#2c4bd8", "#0f766e", "#b45309", "#9f1239", "#7c3aed", "#0284c7"]


# --------------------------------------------------------------------- controls
def _instructor_value(practical_id: str, ctrl: dict, seed: int):
    """Pick a repeatable value for an instructor-only control.

    Students should not know the true value in advance, but a new trial should
    still mean a new object: the choice is seeded by the practical, the control
    and the trial number so reruns stay stable.
    """
    if ctrl["type"] not in {"slider", "number"}:
        return ctrl["default"]
    lo, hi, step = float(ctrl["min"]), float(ctrl["max"]), float(ctrl["step"])
    rng = random.Random(f"{practical_id}::{ctrl['key']}::{seed}")
    value = lo + rng.random() * (hi - lo)
    return round(round(value / step) * step, 6)


def _build_controls(practical: dict, teacher_mode: bool, stacked: bool = False) -> dict:
    controls = practical.get("controls", [])
    params: dict = {}
    visible = []
    seed = st.session_state.get("seed", 1)
    for ctrl in controls:
        if ctrl.get("teacher_only") and not teacher_mode:
            # The student never sees this value: the instructor hands out a fresh
            # object/sample for every trial, so the apparatus itself changes too.
            params[ctrl["key"]] = _instructor_value(practical["id"], ctrl, seed)
        else:
            visible.append(ctrl)

    params.update(practical.get("fixed", {}))

    if not visible:
        return params

    cols = None if stacked else st.columns(min(3, len(visible)))
    for i, ctrl in enumerate(visible):
        unit = ctrl.get("unit", "")
        label = f"{ctrl['label']} ({unit})" if unit else ctrl["label"]
        key = f"{practical['id']}::{ctrl['key']}"
        with (st.container() if cols is None else cols[i % len(cols)]):
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


# ------------------------------------------------------------------------ chart
def _figure(result: dict) -> go.Figure | None:
    series = result.get("series") or []
    if not series:
        return None

    fig = go.Figure()
    for i, s in enumerate(series):
        name = s.get("name", "")
        x, y = s.get("x", []), s.get("y", [])
        colour = PALETTE[i % len(PALETTE)]
        highlighted = name.lower().startswith(("your", "endpoint", "observed", "mean"))

        if s.get("type") == "bar":
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    name=name,
                    marker=dict(
                        color=colour,
                        line=dict(color="#ffffff", width=1),
                    ),
                    opacity=0.9,
                    hovertemplate="%{x}<br>%{y}<extra>" + name + "</extra>",
                )
            )
            continue

        mode = s.get("mode") or ("lines+markers" if len(x) <= 30 else "lines")
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name=name,
                mode=mode,
                line=dict(width=3 if highlighted else 2.6, color=colour),
                marker=dict(
                    size=14 if highlighted else (10 if len(x) <= 30 else 6),
                    symbol="diamond" if highlighted else "circle",
                    color=colour,
                    line=dict(width=2, color="#ffffff"),
                ),
                hovertemplate="%{x}<br>%{y}<extra>" + name + "</extra>",
            )
        )

        # Label a single measured point so students can find their own reading.
        if highlighted and len(x) == 1:
            fig.add_annotation(
                x=x[0],
                y=y[0],
                text=f"{name}: ({x[0]:g}, {y[0]:.3g})",
                showarrow=True,
                arrowhead=2,
                arrowcolor=colour,
                ax=46,
                ay=-38,
                font=dict(size=12, color=colour),
                bgcolor="rgba(255,255,255,.92)",
                bordercolor=colour,
                borderwidth=1,
            )

    fig.update_layout(
        height=430,
        margin=dict(l=14, r=18, t=34, b=14),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#fbfdff",
        font=dict(family="Inter, system-ui, sans-serif", size=13, color="#334155"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=12),
        ),
        hovermode="x unified",
        bargap=0.34,
    )
    fig.update_xaxes(
        title_text=result.get("x_label", ""),
        gridcolor="#e6ebf5",
        zeroline=False,
        linecolor="#94a3b8",
        ticks="outside",
        tickcolor="#cbd5e1",
        title_font=dict(size=13, color="#475569"),
    )
    fig.update_yaxes(
        title_text=result.get("y_label", ""),
        gridcolor="#e6ebf5",
        zeroline=True,
        zerolinecolor="#cbd5e1",
        linecolor="#94a3b8",
        ticks="outside",
        tickcolor="#cbd5e1",
        title_font=dict(size=13, color="#475569"),
    )
    return fig


# ---------------------------------------------------------------------- results
def _verdict(error: float, tolerance: float) -> tuple[str, str]:
    if error <= tolerance * 100:
        return "success", (
            f"Within experimental error ({error:.2f} % ≤ {tolerance * 100:.0f} %). "
            "The result is accepted."
        )
    return "error", (
        f"Outside experimental error ({error:.2f} % > {tolerance * 100:.0f} %). "
        "Check the procedure, look for a systematic error, and repeat the readings."
    )


def _visible_extras(result: dict, quantity: dict | None) -> list[tuple[str, str, str]]:
    """Drop extras that simply repeat the headline measurement."""
    extras = list(result.get("extras") or [])
    if quantity:
        label = quantity.get("label", "").lower()
        unit = quantity.get("unit", "")
        extras = [e for e in extras if e[0].lower() != label]
        if len(extras) == 1 and unit and extras[0][2] == unit:
            extras = []
    return extras


def _result_panel(practical: dict, result: dict) -> float | None:
    q = practical.get("quantity")
    error = None
    extras = _visible_extras(result, q)

    if q and result.get("kind") == "quantitative":
        measured = result["measured"]
        accepted = result["accepted"]
        error = abs(measured - accepted) / abs(accepted) * 100 if accepted else 0.0
        d = q.get("decimals", 2)
        unit = q.get("unit", "")

        left, right = st.columns([1.05, 1.25])
        with left:
            theme.instrument(
                q["label"],
                f"{measured:.{d}f}",
                unit,
                f"accepted {accepted:.{d}f} {unit} · deviation {error:.2f} %",
            )
        with right:
            kind, message = _verdict(error, q["tolerance"])
            if kind == "success":
                st.success(message)
            else:
                st.error(message)

            if result.get("observation"):
                obs = result["observation"]
                theme.observation(
                    obs["colour"], obs["value"], obs.get("label", "Observation")
                )

        if extras:
            st.write("")
            cols = st.columns(len(extras))
            for col, (label, value, unit) in zip(cols, extras):
                col.metric(label, f"{value} {unit}".strip())

    elif result.get("observation"):
        obs = result["observation"]
        theme.observation(obs["colour"], obs["value"], obs.get("label", "Observation"))

        if extras:
            cols = st.columns(len(extras))
            for col, (label, value, unit) in zip(cols, extras):
                col.metric(label, f"{value} {unit}".strip())

    elif extras:
        cols = st.columns(len(extras))
        for col, (label, value, unit) in zip(cols, extras):
            col.metric(label, f"{value} {unit}".strip())

    return error


# ----------------------------------------------------------------------- report
def _report(practical: dict, result: dict, error: float | None) -> str:
    q = practical.get("quantity")
    depth = practical.get("depth") or {}
    syllabus = practical.get("syllabus") or {}

    lines = [
        f"# {practical['title']}",
        "",
        f"*{practical.get('subtitle', '')}*  ",
        f"Class {practical.get('grade', '')} · AKU-EB  ",
    ]
    if syllabus.get("ref"):
        lines.append(f"Syllabus: {syllabus['ref']} — {syllabus.get('activity', '')}")
    if syllabus.get("note"):
        lines.append(f"Fidelity note: {syllabus['note']}")

    if depth.get("objectives"):
        lines += ["", "## Learning objectives", *[f"- {o}" for o in depth["objectives"]]]

    lines += [
        "",
        "## Theory",
        practical.get("theory", ""),
    ]
    if depth.get("formula"):
        lines += ["", "```", depth["formula"], "```"]
    if depth.get("context"):
        lines += ["", f"**Why it matters.** {depth['context']}"]

    lines += [
        "",
        "## Apparatus",
        *[f"- {a}" for a in practical.get("apparatus", [])],
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
        lines.append(f"- {obs.get('label', 'Observation')}: **{obs['value']}**")

    for note in result.get("notes", []):
        lines += ["", f"> {note}"]

    precautions = depth.get("precautions") or [
        "Read all instruments at eye level to avoid parallax error.",
        "Repeat readings and take a mean.",
        "Record readings to the correct number of decimal places.",
    ]
    lines += ["", "## Precautions", *[f"- {p}" for p in precautions]]

    if depth.get("errors"):
        lines += ["", "## Sources of error", *[f"- {e}" for e in depth["errors"]]]
    if depth.get("exam"):
        lines += ["", "## Exam tips", *[f"- {e}" for e in depth["exam"]]]

    viva = list(practical.get("viva", [])) + list(depth.get("viva", []))
    if viva:
        lines += ["", "## Viva questions"]
        for i, qa in enumerate(viva, 1):
            lines += [f"**Q{i}. {qa['q']}**", "", qa["a"], ""]

    return "\n".join(lines)


# ------------------------------------------------------------------- subpages
def _theory_tab(practical: dict) -> None:
    depth = practical.get("depth") or {}

    if depth.get("objectives"):
        st.markdown("#### Learning objectives")
        for objective in depth["objectives"]:
            st.markdown(f"- {objective}")
        st.write("")

    st.markdown("#### Theory")
    paragraphs = depth.get("theory") or [practical.get("theory", "")]
    theme.theory_block(paragraphs)

    if depth.get("formula"):
        theme.formula(depth["formula"])

    if depth.get("context"):
        theme.insight("Why it matters.", depth["context"])

    if not depth:
        st.info(
            "Extended notes for this practical are on the way. The core theory, method and "
            "viva questions are complete below."
        )


def _method_tab(practical: dict) -> None:
    depth = practical.get("depth") or {}
    left, right = st.columns([1, 1.45])

    with left:
        st.markdown("#### Apparatus")
        for item in practical.get("apparatus", []):
            st.markdown(f"- {item}")

        if depth.get("precautions"):
            st.markdown("#### Precautions")
            for item in depth["precautions"]:
                st.markdown(f"- {item}")

        if depth.get("errors"):
            st.markdown("#### Where the result goes wrong")
            for item in depth["errors"]:
                st.markdown(f"- {item}")

    with right:
        st.markdown("#### Procedure")
        for i, step in enumerate(practical.get("procedure", []), 1):
            st.markdown(f"**{i}.** {step}")


def _viva_tab(practical: dict) -> None:
    depth = practical.get("depth") or {}
    core = practical.get("viva", [])
    extra = depth.get("viva", [])

    if depth.get("exam"):
        st.markdown("#### Exam technique")
        for tip in depth["exam"]:
            st.markdown(f"- {tip}")
        st.write("")

    st.markdown("#### Viva questions")
    st.caption(
        "Try answering aloud before opening the model answer — that is how the viva is marked."
    )
    for i, qa in enumerate(core + extra, 1):
        with st.expander(f"Q{i}. {qa['q']}"):
            st.markdown(qa["a"])


def _lab_tab(practical: dict) -> None:
    teacher_mode = st.session_state.get("teacher_mode", False)

    st.markdown("#### 1 · Set up the apparatus")

    if "seed" not in st.session_state:
        st.session_state.seed = 1

    stage_col, control_col = st.columns([3, 2], gap="large")

    with control_col:
        st.markdown("**Controls**")
        if st.button("🔄 New set of readings", width="stretch", type="primary"):
            st.session_state.seed += 1
        params = _build_controls(practical, teacher_mode, stacked=True)
        st.caption(f"Trial run #{st.session_state.seed}")
        if teacher_mode:
            st.info("Teacher mode is on: instructor-only values are visible.")

    engine = registry.get_engine(practical["engine"])
    result = engine(**params, seed=st.session_state.seed)

    with stage_col:
        bench.scene(practical, params, result)
        st.caption(
            "The apparatus is live: move the controls and it responds. Each new set of "
            "readings changes the unknown sample and the measurement error, as a real "
            "experiment would."
        )

    student_titre = None
    if practical.get("canvas") == "titration":
        from ui import canvas as canvas_ui

        st.markdown("#### 2 · Perform the titration")
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
                    "app calculates the concentration from *your* reading."
                )

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

    st.write("")
    st.divider()
    st.markdown("#### Take the reading")
    error = _result_panel(practical, result)

    fig = _figure(result)
    if fig is not None:
        st.write("")
        st.plotly_chart(fig, width="stretch")

    if result.get("table"):
        st.markdown("#### Observation table")
        st.dataframe(result["table"], width="stretch", hide_index=True)

    for note in result.get("notes", []):
        theme.insight("Reading the graph.", note)

    st.write("")
    st.download_button(
        "⬇️ Download lab report (.md)",
        data=_report(practical, result, error),
        file_name=f"{practical['id']}-report.md",
        mime="text/markdown",
    )


# ------------------------------------------------------------------- navigation
def _go_to(practical_id: str) -> None:
    """Callback: make another practical the current page."""
    from content import by_id

    target = by_id(practical_id)
    st.session_state["subject_choice"] = target["subject"]
    st.session_state[f"grade_choice_{target['subject']}"] = "All"
    st.session_state["practical_choice"] = practical_id


def _go_home() -> None:
    st.session_state["subject_choice"] = "home"
    st.session_state.pop("practical_choice", None)


def _jump_to(key: str) -> None:
    _go_to(st.session_state[key])


def practical_switcher(practical: dict) -> None:
    """A switch bar that stays visible on the practical page.

    The sidebar is collapsed by default on phones, and after opening a deep
    link it is easy to feel stuck on one practical. These controls let a
    student move to any other practical, or back home, without hunting for the
    sidebar.
    """
    from content import PRACTICALS, by_id

    ids = [p["id"] for p in PRACTICALS]
    here = ids.index(practical["id"])
    previous_id = ids[here - 1] if here > 0 else ids[-1]
    next_id = ids[(here + 1) % len(ids)]

    with st.container(border=True, key="practical-switcher"):
        nav = st.columns([3.4, 0.9, 0.9, 0.9], vertical_alignment="bottom")
        with nav[0]:
            key = f"jump::{practical['id']}"
            st.selectbox(
                "Switch practical",
                options=ids,
                index=here,
                key=key,
                on_change=_jump_to,
                args=(key,),
                format_func=lambda pid: (
                    f"{by_id(pid)['title']}  ·  {by_id(pid)['subject'].title()} "
                    f"class {by_id(pid)['grade']}"
                ),
            )
        nav[1].button("🏠 Home", width="stretch", on_click=_go_home)
        nav[2].button(
            "← Previous", width="stretch", on_click=_go_to, args=(previous_id,)
        )
        nav[3].button("Next →", width="stretch", on_click=_go_to, args=(next_id,))


# ---------------------------------------------------------------------- render
def render(practical: dict) -> None:
    from content import SUBJECTS, level_of

    practical_switcher(practical)

    subject = practical.get("subject", "")
    meta = SUBJECTS.get(subject, {})
    level = level_of(practical["grade"])
    syllabus = practical.get("syllabus") or {}

    chips = [
        (f"{meta.get('icon', '')} {meta.get('label', subject.title())}", "chip-neutral"),
        (f"Class {practical['grade']} · {level}", "chip-neutral"),
    ]
    if syllabus.get("ref"):
        chips.append((syllabus["ref"], "chip-syllabus"))
    if syllabus.get("activity"):
        chips.append((f"Activity: {syllabus['activity']}", "chip-syllabus"))

    theme.page_header(
        crumbs="Practical · AKU-EB 2025–26 · Virtual Science Lab",
        title=practical["title"],
        subtitle=practical.get("subtitle", ""),
        chips=chips,
    )

    if syllabus.get("note"):
        theme.warning("How this simulation differs.", syllabus["note"])
    if not syllabus.get("ref"):
        theme.warning(
            "Syllabus link not recorded.",
            "This practical has no official reference attached, so double-check it against "
            "your AKU-EB practical table before teaching it.",
        )

    tab_lab, tab_theory, tab_method, tab_viva = st.tabs(
        ["🔬 Lab bench", "📘 Theory", "🧪 Apparatus & method", "🎓 Viva & exam"]
    )

    with tab_lab:
        _lab_tab(practical)
    with tab_theory:
        _theory_tab(practical)
    with tab_method:
        _method_tab(practical)
    with tab_viva:
        _viva_tab(practical)
