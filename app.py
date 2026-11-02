"""Virtual Science Lab — AKU-EB practicals for SSC and HSSC.

Run:  streamlit run app.py
"""

import streamlit as st

from content import GRADES, PRACTICALS, SUBJECTS, by_id, level_of
from content.syllabus_map import OFFICIAL_COUNTS
from ui import renderer, theme

st.set_page_config(
    page_title="Virtual Science Lab — AKU-EB",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="auto",
)

theme.inject()

# Shareable deep links: /?p=bio-osmosis-ix opens that practical directly.
_qp = st.query_params.get("p")
if _qp and st.session_state.get("_last_qp") != _qp:
    _target = by_id(_qp)
    if _target:
        st.session_state["subject_choice"] = _target["subject"]
        st.session_state[f"grade_choice_{_target['subject']}"] = "All"
        st.session_state["practical_choice"] = _target["id"]
    st.session_state["_last_qp"] = _qp


def _open_practical(p: dict) -> None:
    """Callback: jump straight from a home-page card to that practical."""
    st.session_state["subject_choice"] = p["subject"]
    st.session_state[f"grade_choice_{p['subject']}"] = "All"
    st.session_state["practical_choice"] = p["id"]


def _practical_card(p: dict) -> None:
    meta = SUBJECTS[p["subject"]]
    level = level_of(p["grade"])
    with st.container(border=True):
        chips = (
            f'<span class="chip chip-neutral">Class {p["grade"]} · {level}</span>'
            f'<span class="chip chip-syllabus">{meta["label"]}</span>'
        )
        st.markdown(
            f'<div style="min-height:5.6rem">'
            f'<div style="font-weight:700;font-size:1.02rem;color:#0b1220;line-height:1.32;'
            f'font-family:Sora,Inter,sans-serif">{p["title"]}</div>'
            f'<div style="color:#5b6b83;font-size:.9rem;line-height:1.5;margin:.35rem 0 .6rem 0">'
            f'{p.get("subtitle", "")}</div>'
            f"<div>{chips}</div></div>",
            unsafe_allow_html=True,
        )
        st.button(
            "Open practical →",
            key=f"open-{p['id']}",
            width="stretch",
            type="secondary",
            on_click=_open_practical,
            args=(p,),
        )


def home_page() -> None:
    theme.hero(
        "AKU-EB · SSC & HSSC · 2025–26",
        "Virtual Science Lab",
        "Run Physics, Chemistry and Biology practicals on screen. Change the apparatus, "
        "take readings from working instruments, compare your result with the accepted value, "
        "then revise the theory and viva questions that go with it.",
    )

    total_official = sum(sum(g.values()) for g in OFFICIAL_COUNTS.values())
    ssc = sum(1 for p in PRACTICALS if level_of(p["grade"]) == "SSC")
    stats = st.columns(4)
    with stats[0]:
        theme.stat_tile("Practicals", str(len(PRACTICALS)), "simulated end to end")
    with stats[1]:
        theme.stat_tile("Subjects", str(len(SUBJECTS)), "Physics · Chemistry · Biology")
    with stats[2]:
        theme.stat_tile("SSC / HSSC", f"{ssc} / {len(PRACTICALS) - ssc}", "classes IX–X and XI–XII")
    with stats[3]:
        theme.stat_tile("Syllabus activities", str(total_official), "official AKU-EB table")

    st.write("")
    query = st.text_input(
        "Search practicals",
        placeholder="Try: titration, pendulum, osmosis, blood pressure…",
        label_visibility="collapsed",
    ).strip().lower()

    matches = [
        p
        for p in PRACTICALS
        if not query
        or query in p["title"].lower()
        or query in p.get("subtitle", "").lower()
        or query in p["subject"].lower()
        or query in (p.get("syllabus") or {}).get("activity", "").lower()
    ]

    if query:
        st.markdown(f"#### {len(matches)} result(s) for “{query}”")
        if not matches:
            st.info("Nothing matched. Try a shorter word, or browse by subject below.")
        cols = st.columns(3)
        for i, p in enumerate(matches):
            with cols[i % 3]:
                _practical_card(p)
        return

    for key, meta in SUBJECTS.items():
        items = [p for p in PRACTICALS if p["subject"] == key]
        if not items:
            continue

        st.write("")
        st.markdown(
            f'<div style="display:flex;align-items:baseline;gap:.7rem;margin:.4rem 0 .9rem 0">'
            f'<div style="font-family:Sora,Inter,sans-serif;font-size:1.35rem;font-weight:700;'
            f'color:#0b1220">{meta["icon"]} {meta["label"]}</div>'
            f'<div style="color:#7c8aa0;font-size:.88rem">{len(items)} practicals · '
            f'{sum(1 for p in items if level_of(p["grade"]) == "SSC")} SSC · '
            f'{sum(1 for p in items if level_of(p["grade"]) == "HSSC")} HSSC</div></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for i, p in enumerate(items):
            with cols[i % 3]:
                _practical_card(p)

    st.write("")
    theme.insight(
        "Every practical is traceable.",
        "Each simulation names the exact AKU-EB topic and activity it covers. Open "
        "<b>Syllabus coverage</b> in the sidebar to see the official reference for every "
        "practical and the activities still to be built.",
    )


def coverage_page() -> None:
    total_official = sum(sum(g.values()) for g in OFFICIAL_COUNTS.values())
    theme.page_header(
        crumbs="Reference · AKU-EB 2025–26",
        title="Syllabus coverage",
        subtitle="Every practical in this app is traced to a line in the official AKU-EB "
        "topic-wise practical table. No practical has been invented.",
        chips=[("36 simulated", "chip-syllabus"), ("205 official activities", "chip-neutral")],
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        theme.stat_tile("Practicals simulated", str(len(PRACTICALS)), "full simulation + theory")
    with c2:
        theme.stat_tile("Syllabus activities", str(total_official), "listed across all subjects")
    with c3:
        theme.stat_tile(
            "Coverage", f"{len(PRACTICALS) / total_official * 100:.0f}%", "of the practical table"
        )

    st.write("")
    for key, meta in SUBJECTS.items():
        items = [p for p in PRACTICALS if p["subject"] == key]
        if not items:
            continue
        st.markdown(f"#### {meta['icon']} {meta['label']}")

        rows = []
        for grade in GRADES:
            official = OFFICIAL_COUNTS.get(key, {}).get(grade)
            if official is None:
                continue
            built = sum(1 for p in items if p["grade"] == grade)
            rows.append(
                {
                    "Class": grade,
                    "Level": level_of(grade),
                    "Simulated": built,
                    "Activities in syllabus": official,
                    "Coverage": f"{built / official * 100:.0f}%",
                }
            )
        st.dataframe(rows, width="stretch", hide_index=True)

        with st.expander(f"See the {len(items)} practicals and their syllabus lines"):
            detail = []
            for p in items:
                syl = p.get("syllabus") or {}
                detail.append(
                    {
                        "Practical": p["title"],
                        "Class": p["grade"],
                        "Official reference": syl.get("ref", "—"),
                        "Activity": syl.get("activity", "—"),
                        "Fidelity note": syl.get("note", ""),
                    }
                )
            st.dataframe(detail, width="stretch", hide_index=True)
        st.write("")

    theme.warning(
        "Why coverage is not 100%.",
        "The syllabus tables contain many purely observational activities — prepared slides, "
        "specimens, dissections and models (for example the frog specimen, plant and animal "
        "tissues, and the goat heart). These need microscope images and 3D models, which are "
        "the next phase of the project.",
    )
    theme.warning(
        "Fidelity notes.",
        "Two practicals use a measurable method that differs from the one named in the "
        "syllabus: osmosis uses potato tissue instead of cellophane and a thistle funnel, and "
        "the microscope practical assesses magnification and field of view rather than focusing "
        "technique. Both are flagged on the practical page.",
    )


def _reset_practical() -> None:
    st.session_state.pop("practical_choice", None)


with st.sidebar:
    st.markdown(
        '<div style="font-family:Sora,Inter,sans-serif;font-size:1.3rem;font-weight:700">'
        "🧪 Virtual Lab</div>"
        '<div style="color:#9fb3cf;font-size:.8rem;margin-top:.15rem">'
        "AKU-EB · SSC &amp; HSSC · 2025–26</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    subject = st.radio(
        "Subject",
        options=["home", *SUBJECTS, "coverage"],
        format_func=lambda s: {
            "home": "🏠 Home",
            "coverage": "📋 Syllabus coverage",
        }.get(s, f"{SUBJECTS[s]['icon']} {SUBJECTS[s]['label']}" if s in SUBJECTS else s),
        key="subject_choice",
        on_change=_reset_practical,
    )

    selected = None
    if subject not in ("home", "coverage"):
        grade = st.selectbox("Class", ["All", *GRADES], key=f"grade_choice_{subject}")
        items = [
            p
            for p in PRACTICALS
            if p["subject"] == subject and (grade == "All" or p["grade"] == grade)
        ]
        if items:
            chosen = st.selectbox(
                "Practical",
                options=[p["id"] for p in items],
                format_func=lambda pid: f"{by_id(pid)['title']}  ·  {by_id(pid)['grade']}",
                key="practical_choice",
            )
            selected = by_id(chosen)
        else:
            st.info("No practicals for this class yet.")

    st.divider()
    st.session_state.teacher_mode = st.toggle(
        "Teacher mode",
        value=st.session_state.get("teacher_mode", False),
        help="Reveal instructor-only values (true concentration, true diameter, spring stiffness).",
    )
    st.caption(f"{len(PRACTICALS)} practicals loaded")

    with st.expander("How to use the lab"):
        st.markdown(
            "1. Pick a subject and class.\n"
            "2. Set the apparatus on the **Lab bench**.\n"
            "3. Change a control and read the instrument.\n"
            "4. Download the report and revise the **Viva & exam** tab."
        )

if subject == "coverage":
    coverage_page()
elif selected is None:
    home_page()
else:
    renderer.render(selected)

theme.footer()
