"""Vector apparatus scenes for the lab bench.

Each practical gets a line-drawn apparatus stage above its controls so the page
reads like a bench in a real laboratory. The drawings are deliberately
schematic — they show the equipment, its scale and the reading point, not a
photograph.
"""

from __future__ import annotations

import textwrap

import streamlit as st

_METAL = "#cbd5e1"
_DARK = "#334155"
_GLASS = "rgba(186,230,253,.42)"
_LIQUID = "rgba(56,189,248,.38)"


def _frame(inner: str, caption: str) -> str:
    # Blank lines would split the raw HTML into separate Markdown blocks, and
    # Streamlit only passes the first block through unsanitised.
    body = "\n".join(
        line
        for line in textwrap.dedent(inner).strip().splitlines()
        if line.strip()
    )
    return (
        '<div class="bench-stage">'
        '<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" role="img">'
        "<defs>"
        '<linearGradient id="wallG" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#eef4fb"/><stop offset="1" stop-color="#dce7f5"/>'
        "</linearGradient>"
        '<linearGradient id="topG" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#d3a374"/><stop offset="1" stop-color="#a9764a"/>'
        "</linearGradient>"
        '<linearGradient id="metalG" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#f1f5f9"/><stop offset=".55" stop-color="#cbd5e1"/>'
        '<stop offset="1" stop-color="#94a3b8"/>'
        "</linearGradient>"
        '<linearGradient id="glassG" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="rgba(186,230,253,.20)"/>'
        '<stop offset=".45" stop-color="rgba(186,230,253,.55)"/>'
        '<stop offset="1" stop-color="rgba(186,230,253,.20)"/>'
        "</linearGradient>"
        "</defs>"
        '<rect width="640" height="300" fill="url(#wallG)"/>'
        '<rect y="228" width="640" height="72" fill="url(#topG)"/>'
        '<rect y="228" width="640" height="5" fill="#8a5a36" opacity=".55"/>'
        '<rect y="288" width="640" height="12" fill="#7c4f30" opacity=".45"/>'
        f"{body}"
        "</svg>"
        f'<div class="bench-caption">{caption}</div>'
        "</div>"
    )


def _ticks(x: float, y: float, n: int, dx: float, height: float = 9, colour: str = "#64748b") -> str:
    return "".join(
        f'<line x1="{x + i * dx:.1f}" y1="{y}" x2="{x + i * dx:.1f}" y2="{y + (height if i % 5 == 0 else height * .55):.1f}" '
        f'stroke="{colour}" stroke-width="1.2"/>'
        for i in range(n)
    )


# ------------------------------------------------------------------ individual
def _caliper() -> str:
    return _frame(
        f"""
        <rect x="96" y="104" width="468" height="30" rx="7" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(110, 108, 45, 9.6, 9)}
        <rect x="96" y="104" width="30" height="92" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="96" y="180" width="46" height="18" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="300" y="104" width="26" height="108" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="300" y="196" width="62" height="18" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="330" y="168" width="78" height="34" rx="14" fill="#e2e8f0" stroke="{_DARK}" stroke-width="2"/>
        <line x1="330" y1="168" x2="330" y2="202" stroke="{_DARK}" stroke-width="1.2" opacity=".5"/>
        <circle cx="386" cy="160" r="12" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <text x="470" y="196" font-family="Inter,sans-serif" font-size="13" fill="#475569">object between the jaws</text>
        """,
        "Vernier callipers · read the main scale, then the coinciding vernier division",
    )


def _screw_gauge() -> str:
    return _frame(
        f"""
        <path d="M400 82 q74 0 74 74 q0 74 -74 74" fill="none" stroke="url(#metalG)" stroke-width="20"/>
        <path d="M400 82 q74 0 74 74 q0 74 -74 74" fill="none" stroke="{_DARK}" stroke-width="2" opacity=".55"/>
        <rect x="190" y="142" width="120" height="24" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="310" y="128" width="66" height="52" rx="8" fill="#e2e8f0" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(316, 132, 8, 7, 10, "#475569")}
        <rect x="376" y="138" width="34" height="32" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="404" cy="154" r="20" fill="none" stroke="{_DARK}" stroke-width="2" stroke-dasharray="3 3"/>
        <rect x="300" y="176" width="58" height="12" rx="4" fill="#94a3b8" stroke="{_DARK}" stroke-width="1.5"/>
        <text x="186" y="200" font-family="Inter,sans-serif" font-size="13" fill="#475569">wire between the studs</text>
        <text x="196" y="118" font-family="Inter,sans-serif" font-size="12" fill="#64748b">main scale</text>
        <text x="330" y="116" font-family="Inter,sans-serif" font-size="12" fill="#64748b">circular scale</text>
        """,
        "Screw gauge · turn the ratchet until it just grips the wire",
    )


def _balance() -> str:
    return _frame(
        f"""
        <rect x="150" y="90" width="340" height="18" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(160, 108, 35, 9.4, 8)}
        <polygon points="320,108 296,150 344,150" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="304" y="150" width="32" height="78" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="266" y="222" width="108" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="220" y1="108" x2="220" y2="146" stroke="{_DARK}" stroke-width="1.5"/>
        <circle cx="220" cy="160" r="14" fill="#f59e0b" stroke="{_DARK}" stroke-width="2"/>
        <text x="206" y="192" font-family="Inter,sans-serif" font-size="12" fill="#475569">W₁</text>
        <line x1="430" y1="108" x2="430" y2="146" stroke="{_DARK}" stroke-width="1.5"/>
        <circle cx="430" cy="162" r="18" fill="#38bdf8" stroke="{_DARK}" stroke-width="2"/>
        <text x="418" y="198" font-family="Inter,sans-serif" font-size="12" fill="#475569">W₂</text>
        <line x1="220" y1="128" x2="320" y2="128" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        <line x1="320" y1="128" x2="430" y2="128" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        """,
        "Principle of moments · balance the rod, then take moments about the pivot",
    )


def _spring() -> str:
    coils = " ".join(
        f"{330 + (14 if i % 2 else -14)},{108 + i * 11}" for i in range(1, 7)
    )
    return _frame(
        f"""
        <rect x="148" y="84" width="18" height="150" rx="4" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="120" y="222" width="74" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="166" y="84" width="174" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="330" y1="96" x2="330" y2="108" stroke="{_DARK}" stroke-width="2"/>
        <polyline points="330,108 {coils} 330,186" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="312" y="186" width="36" height="28" rx="5" fill="#f59e0b" stroke="{_DARK}" stroke-width="2"/>
        <line x1="348" y1="200" x2="390" y2="200" stroke="{_DARK}" stroke-width="1.6"/>
        <rect x="400" y="112" width="16" height="110" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="1.5"/>
        {_ticks(404, 116, 18, 8, 8)}
        <text x="424" y="140" font-family="Inter,sans-serif" font-size="13" fill="#475569">extension x</text>
        """,
        "Hooke's law · add loads and read the extension on the scale",
    )


def _pendulum() -> str:
    return _frame(
        f"""
        <rect x="150" y="80" width="18" height="154" rx="4" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="122" y="222" width="74" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="168" y="80" width="176" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="336" y1="92" x2="360" y2="184" stroke="{_DARK}" stroke-width="1.8"/>
        <circle cx="360" cy="192" r="18" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <path d="M336 92 A 120 120 0 0 1 452 188" fill="none" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="5 5"/>
        <line x1="336" y1="92" x2="336" y2="214" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        <text x="378" y="150" font-family="Inter,sans-serif" font-size="13" fill="#475569">L to centre of bob</text>
        <text x="286" y="236" font-family="Inter,sans-serif" font-size="12" fill="#64748b">time 20 oscillations</text>
        """,
        "Simple pendulum · keep the amplitude below 10° and time many swings",
    )


def _resonance() -> str:
    return _frame(
        f"""
        <rect x="292" y="66" width="58" height="166" rx="6" fill="url(#glassG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="294" y="158" width="54" height="72" rx="4" fill="{_LIQUID}"/>
        <line x1="294" y1="158" x2="348" y2="158" stroke="#0284c7" stroke-width="2"/>
        <rect x="378" y="86" width="16" height="140" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="1.4"/>
        {_ticks(382, 90, 26, 7, 8)}
        <path d="M296 54 q10 -14 20 0 q10 14 20 0" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <line x1="316" y1="54" x2="316" y2="40" stroke="{_DARK}" stroke-width="2"/>
        <text x="400" y="118" font-family="Inter,sans-serif" font-size="13" fill="#475569">water level</text>
        <text x="206" y="150" font-family="Inter,sans-serif" font-size="13" fill="#475569">tuning fork</text>
        <path d="M258 150 q34 -18 34 0" fill="none" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4"/>
        """,
        "Resonance tube · find the loudest point as the water level moves",
    )


def _circuit(variant: str = "resistor") -> str:
    if variant == "series":
        component = f"""
        <path d="M372 92 l10 0 l8 -14 l14 28 l14 -28 l14 28 l8 -14 l10 0" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <text x="406" y="70" font-family="Inter,sans-serif" font-size="12" fill="#475569">R₁</text>
        <path d="M470 92 l10 0 l8 -14 l14 28 l14 -28 l14 28 l8 -14 l10 0" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <text x="512" y="70" font-family="Inter,sans-serif" font-size="12" fill="#475569">R₂</text>
        """
    elif variant == "lamp":
        component = f"""
        <circle cx="470" cy="92" r="24" fill="#fef9c3" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="456" y1="78" x2="484" y2="106" stroke="{_DARK}" stroke-width="2"/>
        <line x1="484" y1="78" x2="456" y2="106" stroke="{_DARK}" stroke-width="2"/>
        <g stroke="#f59e0b" stroke-width="2" opacity=".8">
          <line x1="470" y1="52" x2="470" y2="60"/><line x1="470" y1="124" x2="470" y2="132"/>
          <line x1="430" y1="92" x2="438" y2="92"/><line x1="502" y1="92" x2="510" y2="92"/>
        </g>
        """
    elif variant == "capacitor":
        component = f"""
        <line x1="454" y1="60" x2="454" y2="124" stroke="{_DARK}" stroke-width="4"/>
        <line x1="474" y1="60" x2="474" y2="124" stroke="{_DARK}" stroke-width="4"/>
        <text x="440" y="146" font-family="Inter,sans-serif" font-size="12" fill="#475569">C</text>
        <path d="M500 92 h30" stroke="{_DARK}" stroke-width="2.4"/>
        <text x="522" y="88" font-family="Inter,sans-serif" font-size="12" fill="#475569">R</text>
        <rect x="530" y="78" width="18" height="28" rx="3" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        """
    else:
        component = f"""
        <path d="M430 92 l10 0 l8 -14 l14 28 l14 -28 l14 28 l8 -14 l10 0" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <text x="472" y="68" font-family="Inter,sans-serif" font-size="12" fill="#475569">R</text>
        """

    return _frame(
        f"""
        <path d="M156 92 H546 V206 H156 Z" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="148" y="174" width="18" height="36" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <line x1="157" y1="182" x2="157" y2="202" stroke="{_DARK}" stroke-width="3"/>
        <line x1="148" y1="192" x2="166" y2="192" stroke="{_DARK}" stroke-width="2"/>
        <text x="132" y="168" font-family="Inter,sans-serif" font-size="12" fill="#475569">supply</text>
        <circle cx="256" cy="92" r="20" fill="#fff" stroke="{_DARK}" stroke-width="2.2"/>
        <text x="249" y="97" font-family="Inter,sans-serif" font-size="14" fill="#334155">A</text>
        <circle cx="330" cy="206" r="20" fill="#fff" stroke="{_DARK}" stroke-width="2.2"/>
        <text x="322" y="211" font-family="Inter,sans-serif" font-size="14" fill="#334155">V</text>
        {component}
        <line x1="384" y1="196" x2="430" y2="196" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="430" y1="196" x2="450" y2="186" stroke="{_DARK}" stroke-width="2.4"/>
        <circle cx="458" cy="192" r="4" fill="{_DARK}"/>
        """,
        "Circuit bench · check polarity, close the switch, then take readings",
    )


def _calorimeter() -> str:
    return _frame(
        f"""
        <rect x="240" y="112" width="160" height="112" rx="14" fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="258" y="126" width="124" height="86" rx="9" fill="{_LIQUID}" stroke="{_DARK}" stroke-width="1.4"/>
        <rect x="238" y="104" width="164" height="14" rx="6" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="320" y1="64" x2="320" y2="150" stroke="{_DARK}" stroke-width="4"/>
        <circle cx="320" cy="164" r="9" fill="#ef4444" stroke="{_DARK}" stroke-width="1.5"/>
        <rect x="356" y="78" width="10" height="70" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="1.5"/>
        <line x1="344" y1="104" x2="360" y2="104" stroke="{_DARK}" stroke-width="2"/>
        <text x="272" y="246" font-family="Inter,sans-serif" font-size="13" fill="#475569">insulated calorimeter</text>
        <text x="356" y="66" font-family="Inter,sans-serif" font-size="12" fill="#475569">thermometer</text>
        """,
        "Calorimeter · stir gently and record the highest steady temperature",
    )


def _beaker(liquid: str = _LIQUID, extra: str = "", caption: str = "") -> str:
    return _frame(
        f"""
        <path d="M262 96 L262 210 Q262 224 276 224 L412 224 Q426 224 426 210 L426 96"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.4"/>
        <path d="M264 156 L264 210 Q264 222 276 222 L412 222 Q424 222 424 210 L424 156 Z"
              fill="{liquid}"/>
        <line x1="250" y1="96" x2="438" y2="96" stroke="{_DARK}" stroke-width="2.4"/>
        <g stroke="#64748b" stroke-width="1.4">
          <line x1="426" y1="122" x2="436" y2="122"/><line x1="426" y1="142" x2="436" y2="142"/>
          <line x1="426" y1="162" x2="436" y2="162"/><line x1="426" y1="182" x2="436" y2="182"/>
        </g>
        {extra}
        """,
        caption or "Bench glassware · read the meniscus at eye level",
    )


def _chromatography() -> str:
    return _beaker(
        liquid="rgba(56,189,248,.26)",
        extra=f"""
        <rect x="316" y="46" width="56" height="170" rx="3" fill="#fffdf5" stroke="{_DARK}" stroke-width="1.6"/>
        <line x1="320" y1="150" x2="368" y2="150" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 3"/>
        <circle cx="334" cy="150" r="5" fill="#a855f7"/>
        <circle cx="350" cy="150" r="5" fill="#f59e0b"/>
        <circle cx="334" cy="96" r="4" fill="#a855f7" opacity=".85"/>
        <circle cx="342" cy="84" r="4" fill="#38bdf8" opacity=".85"/>
        <circle cx="354" cy="72" r="4" fill="#f59e0b" opacity=".85"/>
        <text x="388" y="128" font-family="Inter,sans-serif" font-size="12" fill="#475569">solvent front</text>
        <text x="388" y="166" font-family="Inter,sans-serif" font-size="12" fill="#475569">baseline</text>
        """,
        caption="Paper chromatography · keep the baseline above the solvent",
    )


def _conductivity() -> str:
    return _beaker(
        liquid="rgba(56,189,248,.32)",
        extra=f"""
        <rect x="300" y="80" width="12" height="120" rx="3" fill="#475569"/>
        <rect x="368" y="80" width="12" height="120" rx="3" fill="#475569"/>
        <path d="M306 80 V58 H390 V80" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="348" cy="52" r="16" fill="#fef9c3" stroke="{_DARK}" stroke-width="2"/>
        <text x="342" y="57" font-family="Inter,sans-serif" font-size="12" fill="#334155">💡</text>
        <text x="148" y="150" font-family="Inter,sans-serif" font-size="13" fill="#475569">graphite electrodes</text>
        """,
        caption="Conductivity test · mobile ions complete the circuit and light the bulb",
    )


def _solubility() -> str:
    return _beaker(
        liquid="rgba(56,189,248,.30)",
        extra=f"""
        <g fill="#e2e8f0" stroke="#475569" stroke-width="1">
          <rect x="300" y="204" width="15" height="10" rx="2"/>
          <rect x="324" y="208" width="12" height="8" rx="2"/>
          <rect x="352" y="205" width="14" height="9" rx="2"/>
          <rect x="378" y="209" width="11" height="7" rx="2"/>
        </g>
        <line x1="320" y1="60" x2="320" y2="150" stroke="{_DARK}" stroke-width="4"/>
        <circle cx="320" cy="164" r="8" fill="#ef4444" stroke="{_DARK}" stroke-width="1.4"/>
        <text x="338" y="76" font-family="Inter,sans-serif" font-size="12" fill="#475569">thermometer</text>
        <path d="M262 224 h164" stroke="#94a3b8" stroke-width="2"/>
        """,
        caption="Solubility · hold the temperature steady and let undissolved solid settle",
    )


def _osmosis() -> str:
    return _beaker(
        liquid="rgba(74,222,128,.28)",
        extra=f"""
        <rect x="294" y="126" width="26" height="88" rx="11" transform="rotate(-8 307 170)"
              fill="#fcd34d" stroke="#92400e" stroke-width="1.6"/>
        <rect x="342" y="132" width="26" height="82" rx="11" transform="rotate(7 355 173)"
              fill="#fde68a" stroke="#92400e" stroke-width="1.6"/>
        <rect x="386" y="128" width="26" height="86" rx="11" transform="rotate(-5 399 171)"
              fill="#fcd34d" stroke="#92400e" stroke-width="1.6"/>
        <text x="272" y="246" font-family="Inter,sans-serif" font-size="13" fill="#475569">potato cylinders</text>
        """,
        caption="Osmosis · blot the tissue, weigh, soak, then reweigh",
    )


def _photosynthesis() -> str:
    return _frame(
        f"""
        <path d="M236 112 L236 210 Q236 222 248 222 L388 222 Q400 222 400 210 L400 112"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.4"/>
        <path d="M238 146 L238 210 Q238 220 248 220 L388 220 Q398 220 398 210 L398 146 Z"
              fill="rgba(74,222,128,.26)"/>
        <path d="M318 214 q-22 -34 4 -64 q10 -14 4 -36" fill="none" stroke="#15803d" stroke-width="2.6"/>
        <g fill="#22c55e" opacity=".9">
          <ellipse cx="306" cy="170" rx="8" ry="4" transform="rotate(-30 306 170)"/>
          <ellipse cx="328" cy="150" rx="7" ry="4" transform="rotate(28 328 150)"/>
          <ellipse cx="314" cy="132" rx="6" ry="3.4" transform="rotate(-22 314 132)"/>
        </g>
        <path d="M310 112 q6 -22 26 -18" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <line x1="470" y1="70" x2="470" y2="196" stroke="{_DARK}" stroke-width="4"/>
        <path d="M450 196 h40 l-8 14 h-24 z" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="470" cy="66" r="24" fill="#fef08a" stroke="{_DARK}" stroke-width="2"/>
        <g stroke="#f59e0b" stroke-width="2">
          <line x1="446" y1="40" x2="452" y2="48"/><line x1="494" y1="40" x2="488" y2="48"/>
          <line x1="436" y1="66" x2="446" y2="66"/><line x1="504" y1="66" x2="494" y2="66"/>
        </g>
        <text x="430" y="232" font-family="Inter,sans-serif" font-size="12" fill="#475569">lamp at measured distance</text>
        """,
        "Pondweed · count bubbles over a full minute at each light intensity",
    )


def _sav() -> str:
    return _frame(
        f"""
        <rect x="196" y="188" width="290" height="34" rx="6" fill="#f1f5f9" stroke="{_DARK}" stroke-width="2"/>
        <rect x="220" y="150" width="52" height="40" rx="4" fill="#fcd34d" stroke="#92400e" stroke-width="2"/>
        <rect x="300" y="162" width="38" height="28" rx="4" fill="#fde68a" stroke="#92400e" stroke-width="2"/>
        <rect x="362" y="170" width="26" height="20" rx="3" fill="#fcd34d" stroke="#92400e" stroke-width="2"/>
        <text x="216" y="140" font-family="Inter,sans-serif" font-size="12" fill="#475569">2 cm</text>
        <text x="298" y="152" font-family="Inter,sans-serif" font-size="12" fill="#475569">1 cm</text>
        <text x="360" y="162" font-family="Inter,sans-serif" font-size="12" fill="#475569">0.5 cm</text>
        <line x1="502" y1="96" x2="502" y2="214" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(496, 102, 12, 0, 10)}
        <path d="M470 110 l10 0 l8 -12 l14 24 l14 -24 l14 24 l8 -12 l10 0" fill="none" stroke="{_DARK}" stroke-width="1.8" opacity=".7"/>
        <text x="214" y="248" font-family="Inter,sans-serif" font-size="13" fill="#475569">cut equal cubes and compare area to volume</text>
        """,
        "Surface area to volume · smaller cubes expose more surface per unit volume",
    )


def _flame() -> str:
    return _frame(
        f"""
        <rect x="288" y="176" width="64" height="52" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="310" y="146" width="20" height="34" fill="#94a3b8" stroke="{_DARK}" stroke-width="1.6"/>
        <path d="M320 60 q24 34 12 58 q-4 16 -12 24 q-8 -8 -12 -24 q-12 -24 12 -58 z"
              fill="#fbbf24" stroke="#f97316" stroke-width="1.4"/>
        <path d="M320 92 q10 20 5 32 q-3 8 -5 12 q-2 -4 -5 -12 q-5 -12 5 -32 z" fill="#fef3c7"/>
        <line x1="410" y1="110" x2="352" y2="150" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="350" cy="151" r="6" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <text x="416" y="106" font-family="Inter,sans-serif" font-size="12" fill="#475569">nichrome wire loop</text>
        <text x="268" y="250" font-family="Inter,sans-serif" font-size="13" fill="#475569">clean the loop until the flame is colourless</text>
        """,
        "Flame test · observe the colour against a dark background",
    )


def _testtubes() -> str:
    colours = ["#f87171", "#fbbf24", "#a3e635", "#38bdf8", "#c084fc"]
    tubes = "".join(
        f"""
        <path d="M{236 + i * 36} 98 L{236 + i * 36} 208 Q{236 + i * 36} 220 {246 + i * 36} 220
                 Q{256 + i * 36} 220 {256 + i * 36} 208 L{256 + i * 36} 98"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="1.8"/>
        <path d="M{237 + i * 36} 150 L{237 + i * 36} 208 Q{237 + i * 36} 219 {246 + i * 36} 219
                 Q{255 + i * 36} 219 {255 + i * 36} 208 L{255 + i * 36} 150 Z" fill="{c}"/>
        """
        for i, c in enumerate(colours)
    )
    return _frame(
        f"""
        <rect x="196" y="206" width="260" height="16" rx="5" fill="#b45309" stroke="{_DARK}" stroke-width="2"/>
        <rect x="196" y="222" width="260" height="8" rx="4" fill="#92400e"/>
        {tubes}
        <text x="206" y="86" font-family="Inter,sans-serif" font-size="13" fill="#475569">observe colour and precipitate</text>
        """,
        "Test-tube rack · record the observation before adding the next reagent",
    )


def _microscope() -> str:
    return _frame(
        f"""
        <rect x="252" y="214" width="136" height="14" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <path d="M300 214 q0 -70 44 -86 q40 -14 44 34" fill="none" stroke="url(#metalG)" stroke-width="18"/>
        <path d="M300 214 q0 -70 44 -86 q40 -14 44 34" fill="none" stroke="{_DARK}" stroke-width="1.8" opacity=".5"/>
        <rect x="356" y="132" width="74" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="378" y="152" width="34" height="10" rx="3" fill="#e2e8f0" stroke="{_DARK}" stroke-width="1.6"/>
        <rect x="388" y="92" width="14" height="40" rx="4" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="382" y="68" width="26" height="28" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="394" cy="52" r="12" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="394" cy="52" r="5" fill="#bae6fd"/>
        <rect x="348" y="150" width="18" height="6" rx="2" fill="#38bdf8" opacity=".8"/>
        <text x="470" y="90" font-family="Inter,sans-serif" font-size="12" fill="#475569">eyepiece</text>
        <text x="470" y="128" font-family="Inter,sans-serif" font-size="12" fill="#475569">objective</text>
        <text x="470" y="166" font-family="Inter,sans-serif" font-size="12" fill="#475569">stage</text>
        """,
        "Compound microscope · start low power, focus upwards, then change objective",
    )


def _leaf() -> str:
    return _frame(
        f"""
        <path d="M180 168 Q246 74 386 96 Q416 156 336 202 Q250 232 180 168 Z"
              fill="rgba(74,222,128,.55)" stroke="#15803d" stroke-width="2.4"/>
        <path d="M188 166 Q268 156 348 112" fill="none" stroke="#166534" stroke-width="2"/>
        <g stroke="#166534" stroke-width="1.2" opacity=".55">
          <line x1="250" y1="158" x2="274" y2="126"/><line x1="288" y1="146" x2="314" y2="116"/>
          <line x1="320" y1="130" x2="342" y2="108"/><line x1="256" y1="176" x2="286" y2="188"/>
          <line x1="300" y1="166" x2="330" y2="176"/>
        </g>
        <rect x="252" y="150" width="20" height="20" rx="2" fill="#f59e0b" stroke="{_DARK}" stroke-width="1.2"/>
        <rect x="300" y="132" width="20" height="20" rx="2" fill="#f59e0b" stroke="{_DARK}" stroke-width="1.2"/>
        <text x="420" y="120" font-family="Inter,sans-serif" font-size="12" fill="#475569">cobalt chloride paper</text>
        <text x="420" y="142" font-family="Inter,sans-serif" font-size="12" fill="#475569">upper and lower surfaces</text>
        <text x="250" y="232" font-family="Inter,sans-serif" font-size="13" fill="#475569">blue → pink as water is absorbed</text>
        """,
        "Transpiration · compare the time for the paper to turn pink on each surface",
    )


def _flasks() -> str:
    return _frame(
        f"""
        <path d="M236 106 L236 160 L204 218 Q198 228 210 228 L330 228 Q342 228 336 218 L304 160 L304 106 Z"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M214 200 L326 200 L336 218 Q342 228 330 228 L210 228 Q198 228 204 218 Z"
              fill="rgba(74,222,128,.22)"/>
        <path d="M398 106 L398 160 L366 218 Q360 228 372 228 L492 228 Q504 228 498 218 L466 160 L466 106 Z"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M376 200 L488 200 L498 218 Q504 228 492 228 L372 228 Q360 228 366 218 Z"
              fill="rgba(248,113,113,.22)"/>
        <line x1="258" y1="70" x2="258" y2="190" stroke="{_DARK}" stroke-width="3.6"/>
        <circle cx="258" cy="200" r="7" fill="#ef4444" stroke="{_DARK}" stroke-width="1.2"/>
        <line x1="420" y1="70" x2="420" y2="190" stroke="{_DARK}" stroke-width="3.6"/>
        <circle cx="420" cy="200" r="7" fill="#ef4444" stroke="{_DARK}" stroke-width="1.2"/>
        <text x="220" y="250" font-family="Inter,sans-serif" font-size="12" fill="#475569">germinating seeds</text>
        <text x="400" y="250" font-family="Inter,sans-serif" font-size="12" fill="#475569">boiled control</text>
        """,
        "Respiration · compare the temperature rise in living and boiled seeds",
    )


def _dice() -> str:
    def die(x: int, y: int, pips: list[tuple[int, int]]) -> str:
        body = "".join(
            f'<circle cx="{x + px}" cy="{y + py}" r="6" fill="#0f172a"/>' for px, py in pips
        )
        return (
            f'<rect x="{x}" y="{y}" width="104" height="104" rx="18" fill="#fff" '
            f'stroke="{_DARK}" stroke-width="2.4"/>{body}'
        )

    pips_a = [(30, 30), (74, 30), (52, 52), (30, 74), (74, 74)]
    pips_b = [(30, 30), (74, 30), (30, 74), (74, 74)]
    return _frame(
        f"""
        <g transform="rotate(-8 260 160)">{die(208, 108, pips_a)}</g>
        <g transform="rotate(9 400 160)">{die(348, 108, pips_b)}</g>
        <text x="206" y="90" font-family="Inter,sans-serif" font-size="13" fill="#475569">1–3 = T</text>
        <text x="350" y="90" font-family="Inter,sans-serif" font-size="13" fill="#475569">4–6 = t</text>
        <text x="246" y="250" font-family="Inter,sans-serif" font-size="13" fill="#475569">one throw = one offspring</text>
        """,
        "Monohybrid cross · 3 tall : 1 short is a probability, not a guarantee",
    )


def _blood_pressure() -> str:
    return _frame(
        f"""
        <rect x="220" y="120" width="180" height="76" rx="30" fill="#fecaca" stroke="{_DARK}" stroke-width="2.2"/>
        <rect x="238" y="138" width="144" height="40" rx="18" fill="#fca5a5" opacity=".7"/>
        <path d="M400 150 q70 -8 84 52" fill="none" stroke="{_DARK}" stroke-width="3"/>
        <circle cx="490" cy="120" r="52" fill="#f8fafc" stroke="{_DARK}" stroke-width="2.4"/>
        <circle cx="490" cy="120" r="42" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
        <line x1="490" y1="120" x2="512" y2="96" stroke="#dc2626" stroke-width="2.6"/>
        <circle cx="490" cy="120" r="4" fill="{_DARK}"/>
        <text x="476" y="146" font-family="Inter,sans-serif" font-size="12" fill="#475569">mmHg</text>
        <rect x="430" y="188" width="34" height="28" rx="8" fill="#64748b" stroke="{_DARK}" stroke-width="2"/>
        <text x="206" y="224" font-family="Inter,sans-serif" font-size="12" fill="#475569">cuff at heart level</text>
        """,
        "Sphygmomanometer · inflate above systolic, then release slowly and listen",
    )


def _histogram() -> str:
    bars = [(228, 90), (252, 130), (276, 168), (300, 196), (324, 176), (348, 138), (372, 96)]
    return _frame(
        f"""
        <line x1="200" y1="220" x2="460" y2="220" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="200" y1="80" x2="200" y2="220" stroke="{_DARK}" stroke-width="2.4"/>
        {_ticks(204, 220, 8, 32, 8, "#94a3b8")}
        {"".join(f'<rect x="{x}" y="{220 - h}" width="27" height="{h}" fill="#2c4bd8" opacity=".78" stroke="#fff" stroke-width="1.2"/>' for x, h in bars)}
        <text x="294" y="248" font-family="Inter,sans-serif" font-size="13" fill="#475569">height (cm)</text>
        <text x="206" y="72" font-family="Inter,sans-serif" font-size="13" fill="#475569">frequency</text>
        <text x="480" y="130" font-family="Inter,sans-serif" font-size="12" fill="#475569">mean</text>
        <line x1="480" y1="138" x2="330" y2="138" stroke="#b45309" stroke-width="1.6" stroke-dasharray="5 4"/>
        """,
        "Biostatistics · plot the distribution before choosing mean or median",
    )


# ---------------------------------------------------------------------- lookup
_SCENES = {
    "phy-vernier-ix": _caliper,
    "phy-screw-gauge-ix": _screw_gauge,
    "phy-moments-ix": _balance,
    "phy-hooke-ix": _spring,
    "phy-pendulum-x": _pendulum,
    "phy-resonance-x": _resonance,
    "phy-ohm-x": lambda: _circuit("resistor"),
    "phy-series-x": lambda: _circuit("series"),
    "phy-spherometer-xi": lambda: _frame(
        f"""
        <path d="M180 220 Q320 60 460 220" fill="none" stroke="#93c5fd" stroke-width="12" opacity=".7"/>
        <path d="M180 220 Q320 60 460 220" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <rect x="286" y="104" width="68" height="18" rx="5" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="312" y="58" width="16" height="60" rx="5" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="320" cy="52" r="14" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <line x1="286" y1="132" x2="272" y2="176" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="354" y1="132" x2="368" y2="176" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="320" y1="122" x2="320" y2="144" stroke="{_DARK}" stroke-width="2.4"/>
        <line x1="296" y1="86" x2="344" y2="86" stroke="#94a3b8" stroke-width="1.4" stroke-dasharray="4 3"/>
        <text x="392" y="122" font-family="Inter,sans-serif" font-size="13" fill="#475569">sagitta h</text>
        <text x="196" y="90" font-family="Inter,sans-serif" font-size="13" fill="#475569">spherical surface</text>
        """,
        "Spherometer · three legs define the plane, the centre screw measures the sagitta",
    ),
    "phy-specific-heat-xi": _calorimeter,
    "phy-filament-xii": lambda: _circuit("lamp"),
    "phy-rc-xii": lambda: _circuit("capacitor"),
    "chem-chromatography-ix": _chromatography,
    "chem-conductivity-ix": _conductivity,
    "chem-solubility-ix": _solubility,
    "chem-ph-x": lambda: _testtubes(),
    "chem-standardise-naoh-x": lambda: _beaker(
        liquid="rgba(244,114,182,.30)",
        extra="""
        <rect x="300" y="40" width="18" height="140" rx="4" fill="url(#glassG)" stroke="#334155" stroke-width="1.8"/>
        <line x1="302" y1="60" x2="316" y2="60" stroke="#334155" stroke-width="1.2"/>
        <line x1="302" y1="80" x2="316" y2="80" stroke="#334155" stroke-width="1.2"/>
        <line x1="302" y1="100" x2="316" y2="100" stroke="#334155" stroke-width="1.2"/>
        <path d="M309 180 l-8 12 h16 z" fill="#334155"/>
        <text x="340" y="76" font-family="Inter,sans-serif" font-size="13" fill="#475569">burette</text>
        """,
        caption="Titration · run the base in dropwise and swirl after every addition",
    ),
    "chem-oxalic-x": lambda: _beaker(
        liquid="rgba(244,114,182,.30)",
        extra="""
        <rect x="300" y="40" width="18" height="140" rx="4" fill="url(#glassG)" stroke="#334155" stroke-width="1.8"/>
        <path d="M309 180 l-8 12 h16 z" fill="#334155"/>
        <text x="340" y="76" font-family="Inter,sans-serif" font-size="13" fill="#475569">burette</text>
        """,
        caption="Standard solution · read the bottom of the meniscus at eye level",
    ),
    "chem-flame-x": _flame,
    "chem-halide-x": _testtubes,
    "chem-heat-neutralisation-xi": _calorimeter,
    "chem-kmno4-xi": lambda: _beaker(
        liquid="rgba(168,85,247,.32)",
        extra="""
        <rect x="300" y="40" width="18" height="140" rx="4" fill="url(#glassG)" stroke="#334155" stroke-width="1.8"/>
        <path d="M309 180 l-8 12 h16 z" fill="#334155"/>
        <text x="340" y="76" font-family="Inter,sans-serif" font-size="13" fill="#475569">manganate(VII)</text>
        """,
        caption="Redox titration · the first permanent pink is the end point",
    ),
    "chem-salt-analysis-xii": _testtubes,
    "chem-carbonyl-xii": _testtubes,
    "bio-sav-ix": _sav,
    "bio-osmosis-ix": _osmosis,
    "bio-amylase-temp-ix": _testtubes,
    "bio-amylase-ph-ix": _testtubes,
    "bio-photosynthesis-ix": _photosynthesis,
    "bio-transpiration-ix": _leaf,
    "bio-respiration-heat-ix": _flasks,
    "bio-food-tests-xi": _testtubes,
    "bio-microscope-xi": _microscope,
    "bio-biostatistics-x": _histogram,
    "bio-blood-pressure-xi": _blood_pressure,
    "bio-genetics-dice-xii": _dice,
}


def scene(practical: dict) -> None:
    """Render the apparatus stage for a practical, if one is defined."""
    builder = _SCENES.get(practical.get("id", ""))
    if builder is None:
        return
    st.markdown(builder(), unsafe_allow_html=True)
