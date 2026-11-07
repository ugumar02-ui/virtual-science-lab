"""Visual language for the lab: palette, CSS and small HTML components.

All styling lives here so the pages stay declarative. Every helper returns
markup that Streamlit renders with ``unsafe_allow_html``.
"""

import streamlit as st

INK = "#0b1220"
NAVY = "#132a52"
INDIGO = "#2c4bd8"
TEAL = "#0f766e"
AMBER = "#b45309"
ROSE = "#9f1239"

SUBJECT_COLOURS = {
    "physics": ("#2c4bd8", "#e8edff"),
    "chemistry": ("#0f766e", "#e2f6f2"),
    "biology": ("#7c3aed", "#f2ebff"),
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
h1, h2, h3, .lab-title { font-family: 'Sora', 'Inter', sans-serif; letter-spacing: -0.02em; }

.stApp {
  background:
    radial-gradient(1200px 480px at 12% -10%, #e7edff 0%, rgba(231,237,255,0) 60%),
    radial-gradient(900px 420px at 92% 0%, #e6f7f3 0%, rgba(230,247,243,0) 55%),
    #f7f8fc;
}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1280px; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b1220 0%, #132a52 55%, #123f5a 100%);
}
[data-testid="stSidebar"] * { color: #e6edf7 !important; }
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small { color: #9fb3cf !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.12); }
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stSelectbox"] label { color: #cddaf0 !important; }
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.18); color: #fff;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,.16); }
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
  background: rgba(255,255,255,.10) !important; border-color: rgba(255,255,255,.22) !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="select"] > div * {
  color: #e6edf7 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[role="button"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background: #1b3358 !important; border-color: rgba(255,255,255,.24) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div { background: transparent !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
  background: #1b3358 !important; border: 1px solid rgba(255,255,255,.22) !important;
  border-radius: 10px;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] * { color: #e6edf7 !important; }
[data-testid="stSidebar"] details summary,
[data-testid="stSidebar"] details[open] summary {
  color: #ffffff !important; opacity: 1 !important;
}
[data-testid="stSidebar"] details summary p { color: #ffffff !important; }
[data-testid="stSidebar"] div[data-testid="stExpander"],
[data-testid="stSidebar"] details {
  background: rgba(255,255,255,.06) !important; border: 1px solid rgba(255,255,255,.16) !important;
  border-radius: 12px;
}
[data-testid="stSidebar"] div[data-testid="stExpander"] *,
[data-testid="stSidebar"] details * {
  color: #dbe6f7 !important;
}
[data-testid="stSidebar"] div[data-testid="stExpander"] svg,
[data-testid="stSidebar"] details svg { fill: #9fb3cf !important; }

/* ---------- inputs ---------- */
div[data-baseweb="input"], div[data-baseweb="base-input"] {
  background: #fff; border-radius: 12px;
}
div[data-baseweb="input"] {
  border: 1px solid #d6def0; box-shadow: 0 2px 6px rgba(19,42,82,.04);
}
div[data-baseweb="input"] input { color: #0b1220; }
div[data-baseweb="input"] input::placeholder { color: #94a3b8; }

/* hide the deploy chrome, keep the menu */
[data-testid="stAppDeployButton"] { display: none; }

/* ---------- buttons ---------- */
.stButton > button, .stDownloadButton > button {
  border-radius: 12px; font-weight: 600; border: 1px solid #d6def0;
  transition: transform .08s ease, box-shadow .15s ease, background .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-1px); box-shadow: 0 8px 20px rgba(19,42,82,.12);
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #2c4bd8, #0f766e); border: none; color: white;
}

/* ---------- hero ---------- */
.lab-hero {
  position: relative; overflow: hidden; border-radius: 22px; padding: 2.4rem 2.2rem;
  background: linear-gradient(125deg, #0b1220 0%, #172a4d 45%, #0f766e 100%);
  color: #fff; margin-bottom: 1.4rem; box-shadow: 0 22px 50px rgba(11,18,32,.28);
}
.lab-hero:after {
  content: ""; position: absolute; right: -80px; top: -120px; width: 340px; height: 340px;
  background: radial-gradient(circle, rgba(94,234,212,.35), rgba(94,234,212,0) 65%);
}
.lab-hero h1 { font-size: 2.5rem; margin: 0 0 .4rem 0; line-height: 1.1; }
.lab-hero p { margin: 0; max-width: 46rem; color: #c7d6ee; font-size: 1.02rem; line-height: 1.55; }
.lab-hero .kicker {
  display: inline-block; font-size: .74rem; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: #7dd3fc; margin-bottom: .8rem;
}

/* ---------- page header ---------- */
.lab-header {
  border: 1px solid #e2e8f4; background: #ffffff; border-radius: 20px;
  padding: 1.4rem 1.6rem; margin-bottom: 1.1rem;
  box-shadow: 0 12px 30px rgba(19,42,82,.07);
}
.lab-header .crumbs {
  font-size: .76rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
  color: #64748b; margin-bottom: .45rem;
}
.lab-header h1 { font-size: 1.9rem; margin: 0 0 .35rem 0; color: #0b1220; line-height: 1.15; }
.lab-header p { margin: 0 0 .8rem 0; color: #475569; font-size: 1rem; }

/* ---------- chips ---------- */
.chip {
  display: inline-flex; align-items: center; gap: .35rem; padding: .28rem .7rem;
  border-radius: 999px; font-size: .78rem; font-weight: 600; margin-right: .35rem;
  margin-bottom: .25rem; border: 1px solid transparent;
}
.chip-syllabus { background: #eef2ff; color: #2c4bd8; border-color: #dbe4ff; }
.chip-note { background: #fff7e6; color: #b45309; border-color: #ffe3ad; }
.chip-neutral { background: #f1f5f9; color: #334155; border-color: #e2e8f0; }

/* ---------- cards ---------- */
.lab-card {
  border: 1px solid #e2e8f4; border-radius: 18px; padding: 1.15rem 1.2rem;
  background: #fff; height: 100%; box-shadow: 0 8px 22px rgba(19,42,82,.05);
  transition: box-shadow .18s ease, transform .18s ease, border-color .18s ease;
}
.lab-card:hover {
  transform: translateY(-3px); box-shadow: 0 18px 36px rgba(19,42,82,.12);
  border-color: #c7d4ee;
}
.lab-card h4 { margin: .1rem 0 .4rem 0; font-size: 1.02rem; color: #0b1220; line-height: 1.3; }
.lab-card p { margin: 0 0 .75rem 0; color: #5b6b83; font-size: .9rem; line-height: 1.5; }

/* ---------- stat tiles ---------- */
.stat-tile {
  border: 1px solid #e2e8f4; border-radius: 16px; padding: .95rem 1.1rem; background: #fff;
  box-shadow: 0 6px 18px rgba(19,42,82,.05);
}
.stat-tile .k { font-size: .74rem; letter-spacing: .08em; text-transform: uppercase; color: #64748b; font-weight: 600; }
.stat-tile .v { font-size: 1.5rem; font-weight: 700; color: #0b1220; font-family: 'Sora', sans-serif; }
.stat-tile .s { font-size: .8rem; color: #7c8aa0; }

/* ---------- instrument readout ---------- */
.instrument {
  border-radius: 18px; padding: 1.1rem 1.2rem; color: #d1fae5;
  background: linear-gradient(160deg, #0b1220, #102a2a);
  border: 1px solid #14532d; box-shadow: inset 0 0 26px rgba(16,185,129,.12);
}
.instrument .label { font-size: .74rem; letter-spacing: .12em; text-transform: uppercase; color: #6ee7b7; }
.instrument .value {
  font-family: 'Sora', monospace; font-size: 2.1rem; font-weight: 700; color: #ecfdf5;
  line-height: 1.1; margin: .2rem 0 .1rem 0;
}
.instrument .unit { font-size: .95rem; color: #a7f3d0; }
.instrument .meta { font-size: .78rem; color: #86efac; margin-top: .35rem; }

/* ---------- apparatus stage ---------- */
.bench-stage {
  position: relative; overflow: hidden; border-radius: 20px;
  border: 1px solid #dbe4f3; box-shadow: 0 14px 34px rgba(19,42,82,.10);
  margin: .35rem 0 1rem 0; background: #eef4fb;
}
.bench-stage svg { display: block; width: 100%; height: auto; }
.bench-caption {
  background: linear-gradient(90deg, #0b1220, #132a52); color: #dbeafe;
  padding: .55rem .95rem; font-size: .78rem; font-weight: 600;
  letter-spacing: .01em; border-top: 1px solid rgba(255,255,255,.08);
}

/* ---------- live bench motion ---------- */
@keyframes bench-bubble {
  0%   { transform: translateY(0) scale(.7); opacity: 0; }
  22%  { opacity: .95; }
  100% { transform: translateY(-30px) scale(1.12); opacity: 0; }
}
.bench-stage .bub { animation: bench-bubble 2.4s ease-in infinite; }
.bench-stage .bub.b1 { animation-delay: 0s; }
.bench-stage .bub.b2 { animation-delay: .8s; }
.bench-stage .bub.b3 { animation-delay: 1.6s; }

@keyframes bench-flicker {
  0%, 100% { transform: scale(1, 1); opacity: .94; }
  35%      { transform: scale(.94, 1.07) skewX(2deg); opacity: .82; }
  70%      { transform: scale(1.05, .95) skewX(-2deg); opacity: .98; }
}
.bench-stage .flick {
  animation: bench-flicker .85s ease-in-out infinite;
  transform-box: fill-box; transform-origin: 50% 100%;
}

@keyframes bench-glow {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.07); }
}
.bench-stage .glow {
  animation: bench-glow 2.6s ease-in-out infinite;
  transform-box: fill-box; transform-origin: 50% 50%;
}

@keyframes bench-flow { to { stroke-dashoffset: -32; } }
.bench-stage .flow { animation: bench-flow 1.1s linear infinite; }
.bench-stage .flow.slow { animation-duration: 2.6s; }

@keyframes bench-hum {
  0%, 100% { transform: translateX(0); }
  50%      { transform: translateX(1.6px); }
}
.bench-stage .hum { animation: bench-hum .28s ease-in-out infinite; }

@media (prefers-reduced-motion: reduce) {
  .bench-stage .bub,
  .bench-stage .flick,
  .bench-stage .glow,
  .bench-stage .flow,
  .bench-stage .hum { animation: none !important; }
}

/* Clear Streamlit's fixed header so the switch bar is never clipped. */
div[class*="st-key-practical-switcher"] { margin-top: 1.5rem; }
@media (max-width: 640px) {
  /* Keep the three navigation buttons on one row under the full-width picker. */
  div[class*="st-key-practical-switcher"] [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
  }
  div[class*="st-key-practical-switcher"] [data-testid="stHorizontalBlock"] > div {
    width: auto !important;
  }
  div[class*="st-key-practical-switcher"] [data-testid="stHorizontalBlock"] > div:first-child {
    flex: 0 0 100% !important;
  }
  div[class*="st-key-practical-switcher"] [data-testid="stHorizontalBlock"] > div:nth-child(n+2) {
    flex: 1 1 30% !important; min-width: 0 !important;
  }
}


/* ---------- observation tube ---------- */
.obs-card {
  display: flex; align-items: center; gap: 1.1rem; background: #fff;
  border: 1px solid #e2e8f4; border-radius: 18px; padding: 1rem 1.2rem;
  box-shadow: 0 8px 22px rgba(19,42,82,.05);
}
.obs-tube {
  position: relative; width: 46px; height: 92px; flex: 0 0 46px;
  border: 2px solid #cbd5e1; border-top: none;
  border-radius: 0 0 23px 23px; background: linear-gradient(180deg, #f8fafc, #eef2f8);
  overflow: hidden;
}
.obs-tube > i {
  position: absolute; left: 0; right: 0; bottom: 0; height: 62%;
  border-radius: 0 0 21px 21px; display: block;
  box-shadow: inset 0 8px 14px rgba(255,255,255,.35);
}
.obs-card .obs-k { font-size: .74rem; letter-spacing: .1em; text-transform: uppercase; color: #64748b; font-weight: 600; }
.obs-card .obs-v { font-family: 'Sora', sans-serif; font-size: 1.25rem; font-weight: 700; color: #0b1220; }
.obs-card .obs-s { color: #64748b; font-size: .86rem; }

/* ---------- formula ---------- */
.formula {
  background: linear-gradient(160deg, #0b1220, #16294a); color: #dbeafe;
  border-radius: 16px; padding: 1rem 1.2rem; font-family: 'Sora', ui-monospace, monospace;
  font-size: .98rem; line-height: 1.9; white-space: pre-line;
  border: 1px solid #1e3a8a; box-shadow: 0 12px 26px rgba(11,18,32,.16);
  margin: .6rem 0 1rem 0;
}
.formula .tag {
  display: block; font-family: 'Inter', sans-serif; font-size: .7rem; letter-spacing: .14em;
  text-transform: uppercase; color: #7dd3fc; margin-bottom: .35rem; font-weight: 700;
}

/* ---------- highlights ---------- */
.insight {
  border-left: 4px solid #0f766e; background: #f0fdfa; border-radius: 0 14px 14px 0;
  padding: .85rem 1.05rem; margin: .8rem 0; color: #134e4a; line-height: 1.65;
}
.insight b { color: #0f766e; }
.warnbox {
  border-left: 4px solid #b45309; background: #fffbeb; border-radius: 0 14px 14px 0;
  padding: .85rem 1.05rem; margin: .8rem 0; color: #78350f; line-height: 1.65;
}
.warnbox b { color: #b45309; }

/* ---------- theory prose ---------- */
.prose { color: #1e293b; font-size: 1rem; line-height: 1.75; }
.prose h4 { margin: 1.3rem 0 .4rem 0; color: #0b1220; font-size: 1.05rem; }
.prose ul { margin: .3rem 0 .8rem 1.1rem; }
.prose li { margin-bottom: .35rem; }
.prose .why {
  border-left: 3px solid #2c4bd8; background: #f5f7ff; padding: .85rem 1rem;
  border-radius: 0 12px 12px 0; margin: .9rem 0;
}

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: .35rem; border-bottom: 1px solid #e2e8f4; }
.stTabs [data-baseweb="tab"] {
  border-radius: 12px 12px 0 0; padding: .55rem 1rem; font-weight: 600; color: #475569;
}
.stTabs [aria-selected="true"] { background: #eef2ff; color: #2c4bd8 !important; }

/* ---------- misc ---------- */
hr { border-color: #e6ebf5; }
[data-testid="stMetric"] {
  background: #fff; border: 1px solid #e2e8f4; border-radius: 16px;
  padding: .85rem 1rem; box-shadow: 0 6px 18px rgba(19,42,82,.05);
}
[data-testid="stMetricLabel"] { color: #64748b; }
div[data-testid="stExpander"] {
  border: 1px solid #e2e8f4; border-radius: 14px; background: #fff;
}
.lab-footer { margin-top: 2.5rem; color: #7c8aa0; font-size: .82rem; text-align: center; }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(kicker: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="lab-hero">
          <div class="kicker">{kicker}</div>
          <h1>{title}</h1>
          <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(
    crumbs: str,
    title: str,
    subtitle: str,
    chips: list[tuple[str, str]] | None = None,
) -> None:
    chip_html = "".join(
        f'<span class="chip {cls}">{text}</span>' for text, cls in (chips or [])
    )
    st.markdown(
        f"""
        <div class="lab-header">
          <div class="crumbs">{crumbs}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
          <div>{chip_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_tile(label: str, value: str, sub: str = "") -> None:
    st.markdown(
        f"""
        <div class="stat-tile">
          <div class="k">{label}</div>
          <div class="v">{value}</div>
          <div class="s">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def instrument(label: str, value: str, unit: str, meta: str = "") -> None:
    st.markdown(
        f"""
        <div class="instrument">
          <div class="label">{label}</div>
          <div class="value">{value}<span class="unit"> {unit}</span></div>
          <div class="meta">{meta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def theory_block(paragraphs: list[str], bullets: list[str] | None = None) -> None:
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    if bullets:
        body += "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
    st.markdown(f'<div class="prose">{body}</div>', unsafe_allow_html=True)


def formula(text: str, tag: str = "Working equations") -> None:
    st.markdown(
        f'<div class="formula"><span class="tag">{tag}</span>{text}</div>',
        unsafe_allow_html=True,
    )


def insight(title: str, body: str) -> None:
    st.markdown(
        f'<div class="insight"><b>{title}</b> {body}</div>', unsafe_allow_html=True
    )


def warning(title: str, body: str) -> None:
    st.markdown(
        f'<div class="warnbox"><b>{title}</b> {body}</div>', unsafe_allow_html=True
    )


def observation(colour: str, value: str, label: str = "Observation", sub: str = "") -> None:
    st.markdown(
        f"""
        <div class="obs-card">
          <div class="obs-tube"><i style="background:{colour}"></i></div>
          <div>
            <div class="obs-k">{label}</div>
            <div class="obs-v">{value}</div>
            <div class="obs-s">{sub}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        '<div class="lab-footer">Virtual Science Lab · AKU-EB SSC &amp; HSSC practicals · '
        "built for classroom demonstrations and independent practice</div>",
        unsafe_allow_html=True,
    )
