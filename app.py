"""Virtual Science Lab — AKU-EB practicals for SSC and HSSC.

Run:  streamlit run app.py
"""

import streamlit as st

from content import GRADES, PRACTICALS, SUBJECTS, level_of
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


with st.sidebar:
    st.markdown("## 🧪 Virtual Lab")
    st.caption("AKU-EB · SSC & HSSC · 2025–26")
    st.divider()

    subject = st.radio(
        "Subject",
        options=["home", *SUBJECTS],
        format_func=lambda s: "🏠 Home"
        if s == "home"
        else f"{SUBJECTS[s]['icon']} {SUBJECTS[s]['label']}",
    )

    selected = None
    if subject != "home":
        grade = st.selectbox("Class", ["All", *GRADES])
        items = [
            p
            for p in PRACTICALS
            if p["subject"] == subject and (grade == "All" or p["grade"] == grade)
        ]
        if items:
            selected = st.selectbox(
                "Practical",
                options=items,
                format_func=lambda p: f"{p['title']}  ·  {p['grade']}",
            )
        else:
            st.info("No practicals for this class yet.")

    st.divider()
    st.session_state.teacher_mode = st.toggle(
        "Teacher mode",
        value=st.session_state.get("teacher_mode", False),
        help="Reveal instructor-only values (true concentration, true diameter, spring stiffness).",
    )
    st.caption(f"{len(PRACTICALS)} practicals loaded")

if selected is None:
    home_page()
else:
    renderer.render(selected)
