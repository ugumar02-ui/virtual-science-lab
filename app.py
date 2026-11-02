"""Virtual Science Lab — AKU-EB practicals for SSC and HSSC.

Run:  streamlit run app.py
"""

import streamlit as st

from content import GRADES, PRACTICALS, SUBJECTS, by_id, level_of
from content.syllabus_map import OFFICIAL_COUNTS
from ui import renderer

st.set_page_config(
    page_title="Virtual Science Lab — AKU-EB",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem;}
      div[data-testid="stMetricValue"] {font-size: 1.35rem;}
      .hero {
        background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 55%, #047857 100%);
        color: white; padding: 2.2rem 2rem; border-radius: 18px; margin-bottom: 1.5rem;
      }
      .hero h1 {margin: 0 0 .35rem 0; font-size: 2.3rem;}
      .hero p {margin: 0; opacity: .88; font-size: 1.02rem;}
      .badge {
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        font-size: .72rem; font-weight: 600; letter-spacing: .03em;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def _open_practical(p: dict) -> None:
    """Callback: jump straight from a home-page card to that practical."""
    st.session_state["subject_choice"] = p["subject"]
    st.session_state[f"grade_choice_{p['subject']}"] = "All"
    st.session_state["practical_choice"] = p["id"]


def home_page() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>🧪 Virtual Science Lab</h1>
          <p>AKU-EB Physics, Chemistry and Biology practicals for SSC and HSSC.
             Run the experiment, take readings, and check your result against the accepted value.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, (key, meta) in zip(cols, SUBJECTS.items()):
        items = [p for p in PRACTICALS if p["subject"] == key]
        with col:
            st.metric(f"{meta['icon']} {meta['label']}", f"{len(items)} practicals")
            ssc = sum(1 for p in items if level_of(p["grade"]) == "SSC")
            st.caption(f"{ssc} SSC · {len(items) - ssc} HSSC")

    st.divider()

    for key, meta in SUBJECTS.items():
        items = [p for p in PRACTICALS if p["subject"] == key]
        if not items:
            continue
        st.markdown(f"### {meta['icon']} {meta['label']}")
        cols = st.columns(3)
        for i, p in enumerate(items):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{p['title']}**")
                    st.caption(p.get("subtitle", ""))
                    level = level_of(p["grade"])
                    colour = "#1d4ed8" if level == "SSC" else "#047857"
                    st.markdown(
                        f'<span class="badge" style="background:{colour}1a;color:{colour}">'
                        f"Class {p['grade']} · {level}</span>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "Open practical →",
                        key=f"open-{p['id']}",
                        width="stretch",
                        type="secondary",
                        on_click=_open_practical,
                        args=(p,),
                    ):
                        pass


def coverage_page() -> None:
    st.title("📋 Syllabus coverage")
    st.caption(
        "Every practical in this app is traced to a line in the official AKU-EB 2025–26 "
        "topic-wise practical table. No practical has been invented."
    )

    total_official = sum(sum(g.values()) for g in OFFICIAL_COUNTS.values())
    c1, c2, c3 = st.columns(3)
    c1.metric("Practicals simulated", len(PRACTICALS))
    c2.metric("Syllabus activities listed", total_official)
    c3.metric("Subjects", len(SUBJECTS))

    st.divider()

    for key, meta in SUBJECTS.items():
        items = [p for p in PRACTICALS if p["subject"] == key]
        if not items:
            continue
        st.subheader(f"{meta['icon']} {meta['label']}")

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

    st.divider()
    st.markdown(
        """
        **Why coverage is not 100%.** The syllabus tables contain many purely observational
        activities — prepared slides, specimens, dissections and models (for example the frog
        specimen, plant and animal tissues, and the goat heart). These need microscope images
        and 3D models, which is the next phase of the project.

        **Fidelity notes.** Two practicals use a measurable method that differs from the one
        named in the syllabus: osmosis uses potato tissue instead of cellophane and a thistle
        funnel, and the microscope practical assesses magnification and field of view rather
        than focusing technique. Both are flagged on the practical page.
        """
    )


def _reset_practical() -> None:
    st.session_state.pop("practical_choice", None)


with st.sidebar:
    st.markdown("## 🧪 Virtual Lab")
    st.caption("AKU-EB · SSC & HSSC · 2025–26")
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

if subject == "coverage":
    coverage_page()
elif selected is None:
    home_page()
else:
    renderer.render(selected)
