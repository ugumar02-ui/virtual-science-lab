"""Live, parameter-driven apparatus scenes for the lab bench.

Every drawing is a pure function of the current control values (and, where it
helps, the engine result), so moving a slider moves the apparatus: the calliper
jaw opens, the spring stretches, the pendulum swings wider, the burette empties,
the indicator changes colour. A handful of CSS animations (bubbles, flame,
current flow) keep the bench feeling alive between reruns.
"""

from __future__ import annotations

import math
import textwrap

import streamlit as st

_METAL = "#cbd5e1"
_DARK = "#334155"
_GLASS = "rgba(186,230,253,.42)"
_LIQUID = "rgba(56,189,248,.38)"


# ------------------------------------------------------------------- utilities
def _p(params: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(params.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _num(value, fallback: float = 0.0) -> float:
    """Pull the first number out of a value such as '25.02 cm³'."""
    try:
        return float(str(value).replace("−", "-").split()[0])
    except (TypeError, ValueError):
        return fallback


def _tag(x: float, y: float, text: str, colour: str = "#0f766e") -> str:
    width = len(text) * 6.0 + 18
    return (
        f'<g><rect x="{x - width / 2:.1f}" y="{y - 13}" width="{width:.1f}" height="20" '
        f'rx="10" fill="rgba(255,255,255,.95)" stroke="{colour}" stroke-opacity=".4"/>'
        f'<text x="{x:.1f}" y="{y + 1.4}" text-anchor="middle" font-family="Inter,sans-serif" '
        f'font-size="11.5" font-weight="600" fill="{colour}">{text}</text></g>'
    )


def _frame(inner: str, caption: str) -> str:
    # Blank lines would split the raw HTML into separate Markdown blocks, and
    # Streamlit only passes the first block through unsanitised.
    body = "\n".join(
        line for line in textwrap.dedent(inner).strip().splitlines() if line.strip()
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
        '<radialGradient id="shine" cx="50%" cy="35%" r="60%">'
        '<stop offset="0" stop-color="#ffffff" stop-opacity=".75"/>'
        '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
        "</radialGradient>"
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
        f'<line x1="{x + i * dx:.1f}" y1="{y}" x2="{x + i * dx:.1f}" '
        f'y2="{y + (height if i % 5 == 0 else height * .55):.1f}" '
        f'stroke="{colour}" stroke-width="1.2"/>'
        for i in range(max(0, int(n)))
    )


def _tube(cx: float, top: float, bottom: float, width: float, liquid_top: float, colour: str) -> str:
    """A test tube with a rounded base, filled from liquid_top downwards."""
    left, right = cx - width / 2, cx + width / 2
    r = width / 2
    body = (
        f'<path d="M{left:.1f} {top} L{left:.1f} {bottom - r:.1f} '
        f'Q{left:.1f} {bottom} {cx:.1f} {bottom} Q{right:.1f} {bottom} {right:.1f} {bottom - r:.1f} '
        f'L{right:.1f} {top}" fill="url(#glassG)" stroke="{_DARK}" stroke-width="1.8"/>'
    )
    if liquid_top < bottom - r:
        liquid = (
            f'<path d="M{left + 1.5:.1f} {liquid_top:.1f} L{left + 1.5:.1f} {bottom - r:.1f} '
            f'Q{left + 1.5:.1f} {bottom - 1.5:.1f} {cx:.1f} {bottom - 1.5:.1f} '
            f'Q{right - 1.5:.1f} {bottom - 1.5:.1f} {right - 1.5:.1f} {bottom - r:.1f} '
            f'L{right - 1.5:.1f} {liquid_top:.1f} Z" fill="{colour}"/>'
        )
    else:
        liquid = ""
    return body + liquid


def _thermometer(x: float, bulb_y: float, top: float, value: float, lo: float, hi: float) -> str:
    frac = _clamp((value - lo) / (hi - lo), 0.02, 1.0)
    col_top = bulb_y - 10 - frac * (bulb_y - 10 - top)
    return (
        f'<rect x="{x - 5:.1f}" y="{top:.1f}" width="10" height="{bulb_y - top:.1f}" rx="5" '
        f'fill="#f8fafc" stroke="{_DARK}" stroke-width="1.4"/>'
        f'<rect x="{x - 2.4:.1f}" y="{col_top:.1f}" width="4.8" height="{bulb_y - col_top:.1f}" '
        f'rx="2.4" fill="#dc2626"/>'
        f'<circle cx="{x:.1f}" cy="{bulb_y:.1f}" r="7" fill="#dc2626" stroke="{_DARK}" stroke-width="1.2"/>'
    )


def _flame(cx: float, base_y: float, colour: str, scale: float = 1.0, flicker: bool = True) -> str:
    h = 74 * scale
    w = 30 * scale
    cls = ' class="flick"' if flicker else ""
    return (
        f'<g{cls}>'
        f'<path d="M{cx:.1f} {base_y - h:.1f} q{w:.1f} {h * .46:.1f} {w * .5:.1f} {h * .78:.1f} '
        f'q-{w * .17:.1f} {h * .22:.1f} -{w * .5:.1f} {h * .22:.1f} '
        f'q-{w * .33:.1f} 0 -{w * .5:.1f} -{h * .22:.1f} '
        f'q-{w * .17:.1f} -{h * .32:.1f} {w * .5:.1f} -{h * .78:.1f} z" '
        f'fill="{colour}" opacity=".92"/>'
        f'<path d="M{cx:.1f} {base_y - h * .42:.1f} q{w * .34:.1f} {h * .26:.1f} {w * .16:.1f} {h * .42:.1f} '
        f'q-{w * .08:.1f} {h * .12:.1f} -{w * .16:.1f} {h * .12:.1f} '
        f'q-{w * .08:.1f} 0 -{w * .16:.1f} -{h * .12:.1f} '
        f'q-{w * .18:.1f} -{h * .16:.1f} {w * .16:.1f} -{h * .42:.1f} z" '
        f'fill="#fef9c3" opacity=".9"/></g>'
    )


def _weight(x: float, y: float, r: float, colour: str, label: str) -> str:
    return (
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{colour}" stroke="{_DARK}" stroke-width="2"/>'
        f'<circle cx="{x - r * .32:.1f}" cy="{y - r * .36:.1f}" r="{r * .26:.1f}" fill="#fff" opacity=".38"/>'
        f'<text x="{x:.1f}" y="{y + r + 15:.1f}" text-anchor="middle" font-family="Inter,sans-serif" '
        f'font-size="11.5" fill="#475569">{label}</text>'
    )


# --------------------------------------------------------------------- physics
def _caliper(p: dict, r: dict) -> str:
    d = _clamp(_p(p, "true_diameter_mm", 20), 10, 40)
    gap = 22 + (d - 10) * 4.4
    jx = 126 + gap
    beam_end = jx + 118
    reading = _num(r.get("measured"), d)
    zero = _clamp(_p(p, "zero_error_mm", 0.0), -0.1, 0.1)
    # A real zero error shifts the vernier scale by a fraction of a millimetre;
    # exaggerate it so the effect is visible on a 640 px drawing.
    zero_px = _clamp(zero * 90, -14, 14)
    dx = (640 - (beam_end - 96)) / 2 - 96
    return _frame(
        f"""
        <g transform="translate({dx:.1f} 0)">
        <rect x="96" y="104" width="{beam_end - 96:.1f}" height="30" rx="7" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(110, 108, int((beam_end - 116) / 9.6), 9.6, 9)}
        <rect x="96" y="104" width="30" height="92" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="96" y="180" width="46" height="18" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="{jx:.1f}" y="104" width="26" height="108" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="{jx:.1f}" y="196" width="62" height="18" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="{jx + 30:.1f}" y="168" width="78" height="34" rx="14" fill="#e2e8f0" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="{jx + 86:.1f}" cy="160" r="12" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="{126 + gap / 2:.1f}" cy="160" r="{max(9, gap / 2 - 2):.1f}" fill="rgba(56,189,248,.55)" stroke="#0284c7" stroke-width="2"/>
        <g transform="translate({zero_px:.1f} 0)">
          {_ticks(jx + 3, 112, 6, 4.6, 7, "#9f1239")}
          <line x1="{jx + 3:.1f}" y1="112" x2="{jx + 3:.1f}" y2="132" stroke="#9f1239" stroke-width="2"/>
        </g>
        <line x1="126" y1="206" x2="{126 + gap:.1f}" y2="206" stroke="#0f766e" stroke-width="2"/>
        <text x="{126 + gap / 2:.1f}" y="222" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#0f766e">jaw gap</text>
        </g>
        {_tag(320, 74, f"reading {reading:.2f} mm · zero {zero:+.2f} mm")}
        """,
        "Vernier callipers · the sliding jaw opens as the object grows",
    )


def _screw_gauge(p: dict, r: dict) -> str:
    d = _clamp(_p(p, "true_diameter_mm", 0.5), 0.2, 1.0)
    gap = 2 + (d - 0.2) * 18
    zero = _clamp(_p(p, "zero_error_mm", 0.0), -0.02, 0.02)
    # Exaggerate the zero error so a small thimble rotation is visible.
    angle = -140 + ((d / 0.5) % 1.0) * 280 + zero * 900
    reading = _num(r.get("measured"), d)
    wire_left, wire_right = 336, 360 + gap
    return _frame(
        f"""
        <path d="M400 82 q74 0 74 74 q0 74 -74 74" fill="none" stroke="url(#metalG)" stroke-width="20"/>
        <path d="M400 82 q74 0 74 74 q0 74 -74 74" fill="none" stroke="{_DARK}" stroke-width="2" opacity=".55"/>
        <rect x="190" y="142" width="120" height="24" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="310" y="128" width="66" height="52" rx="8" fill="#e2e8f0" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(316, 132, 8, 7, 10, "#475569")}
        <rect x="{360 + gap:.1f}" y="138" width="34" height="32" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <line x1="{wire_left}" y1="182" x2="{wire_right:.1f}" y2="182" stroke="#b45309" stroke-width="{max(2, gap * .45):.1f}"/>
        <circle cx="404" cy="154" r="20" fill="none" stroke="{_DARK}" stroke-width="2" stroke-dasharray="3 3"/>
        <line x1="404" y1="154" x2="{404 + 15 * math.sin(math.radians(angle)):.1f}" y2="{154 - 15 * math.cos(math.radians(angle)):.1f}" stroke="#dc2626" stroke-width="2.4"/>
        <circle cx="404" cy="154" r="3" fill="#dc2626"/>
        <rect x="300" y="176" width="58" height="12" rx="4" fill="#94a3b8" stroke="{_DARK}" stroke-width="1.5"/>
        <text x="330" y="116" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" fill="#64748b">circular scale</text>
        {_tag(300, 74, f"wire {reading:.3f} mm · zero {zero:+.3f} mm")}
        """,
        "Screw gauge · the thimble turns and the studs close on the wire",
    )


def _balance(p: dict, r: dict) -> str:
    w1 = _p(p, "known_weight_n", 2)
    d1 = _clamp(_p(p, "distance_known_cm", 30), 10, 45)
    d2 = _clamp(_p(p, "distance_unknown_cm", 20), 10, 45)
    w2 = _num(r.get("measured"), w1 * d1 / d2)
    x1 = 320 - d1 * 2.8
    x2 = 320 + d2 * 2.8
    r1 = 9 + w1 * 2.2
    r2 = _clamp(9 + w2 * 2.2, 10, 24)
    return _frame(
        f"""
        <rect x="150" y="90" width="340" height="18" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        {_ticks(160, 108, 34, 9.4, 8)}
        <polygon points="320,108 296,150 344,150" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="304" y="150" width="32" height="78" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="266" y="222" width="108" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="{x1:.1f}" y1="108" x2="{x1:.1f}" y2="146" stroke="{_DARK}" stroke-width="1.5"/>
        {_weight(x1, 158, r1, "#f59e0b", "W₁")}
        <line x1="{x2:.1f}" y1="108" x2="{x2:.1f}" y2="146" stroke="{_DARK}" stroke-width="1.5"/>
        {_weight(x2, 160, r2, "#38bdf8", "W₂")}
        <line x1="{x1:.1f}" y1="128" x2="320" y2="128" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        <line x1="320" y1="128" x2="{x2:.1f}" y2="128" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        <text x="{(x1 + 320) / 2:.1f}" y="122" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#64748b">d₁ {d1:.0f} cm</text>
        <text x="{(320 + x2) / 2:.1f}" y="122" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#64748b">d₂ {d2:.0f} cm</text>
        {_tag(320, 74, f"W₂ = W₁d₁/d₂ = {w2:.2f} N")}
        """,
        "Principle of moments · the weights slide as the distances change",
    )


def _spring(p: dict, r: dict) -> str:
    k = _clamp(_p(p, "spring_constant", 25), 5, 60)
    m = _clamp(_p(p, "max_mass_g", 300), 100, 500)
    ext_mm = m * 9.81 / k
    ext_px = _clamp(ext_mm * 0.62, 8, 92)
    top, length = 108, 54 + ext_px
    coils = []
    n = 7
    for i in range(1, n):
        x = 330 + (15 if i % 2 else -15)
        coils.append(f"{x},{top + length * i / n:.1f}")
    coil_path = " ".join(coils)
    block_y = top + length + 2
    return _frame(
        f"""
        <rect x="148" y="84" width="18" height="150" rx="4" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="120" y="222" width="74" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="166" y="84" width="174" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="330" y1="96" x2="330" y2="{top}" stroke="{_DARK}" stroke-width="2"/>
        <polyline points="330,{top} {coil_path} 330,{top + length:.1f}" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="312" y="{block_y:.1f}" width="36" height="30" rx="5" fill="#f59e0b" stroke="{_DARK}" stroke-width="2"/>
        <text x="330" y="{block_y + 20:.1f}" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="#7c2d12">{m:.0f} g</text>
        <line x1="348" y1="{block_y + 15:.1f}" x2="398" y2="{block_y + 15:.1f}" stroke="{_DARK}" stroke-width="1.4"/>
        <rect x="408" y="104" width="16" height="116" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="1.4"/>
        {_ticks(412, 108, 22, 7.4, 8)}
        <line x1="398" y1="{block_y + 15:.1f}" x2="408" y2="{block_y + 15:.1f}" stroke="#dc2626" stroke-width="2.2"/>
        <text x="434" y="134" font-family="Inter,sans-serif" font-size="12" fill="#475569">extension</text>
        {_tag(320, 74, f"k = {k:.0f} N/m · extension = {ext_mm:.0f} mm")}
        """,
        "Hooke's law · add mass and watch the spring extend",
    )


def _pendulum(p: dict, r: dict) -> str:
    length = _clamp(_p(p, "length_cm", 100), 20, 150)
    amp = _clamp(_p(p, "amplitude_deg", 10), 2, 30)
    mass = _clamp(_p(p, "mass_g", 50), 20, 200)
    lpx = 40 + (length - 20) * 1.18
    rad = math.radians(amp)
    bx = 336 + math.sin(rad) * lpx
    by = 92 + math.cos(rad) * lpx
    bob_r = 9 + mass * 0.065
    period = _num(r.get("extras") and r["extras"][0][1], 2.0)
    return _frame(
        f"""
        <rect x="150" y="80" width="18" height="154" rx="4" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="122" y="222" width="74" height="12" rx="5" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="168" y="80" width="176" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="336" y1="92" x2="{bx:.1f}" y2="{by:.1f}" stroke="{_DARK}" stroke-width="1.8"/>
        <circle cx="{bx:.1f}" cy="{by:.1f}" r="{bob_r:.1f}" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <path d="M336 92 A {lpx:.1f} {lpx:.1f} 0 0 1 {336 + math.sin(rad) * lpx:.1f} {92 + math.cos(rad) * lpx:.1f}"
              fill="none" stroke="#94a3b8" stroke-width="1.3" stroke-dasharray="5 5"/>
        <line x1="336" y1="92" x2="336" y2="{92 + lpx + 10:.1f}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 4"/>
        <path d="M336 130 A 38 38 0 0 1 {336 + 38 * math.sin(rad):.1f} {92 + 38 * math.cos(rad):.1f}" fill="none" stroke="#0f766e" stroke-width="1.4"/>
        <text x="{336 + 48 * math.sin(rad / 2):.1f}" y="{92 + 48 * math.cos(rad / 2):.1f}" font-family="Inter,sans-serif" font-size="11" fill="#0f766e">{amp:.0f}°</text>
        <text x="{bx + 26:.1f}" y="{by - 6:.1f}" font-family="Inter,sans-serif" font-size="12" fill="#475569">L = {length:.0f} cm</text>
        {_tag(320, 74, f"T = {period:.3f} s · {mass:.0f} g bob")}
        """,
        "Simple pendulum · length, amplitude and bob all move the swing",
    )


def _resonance(p: dict, r: dict) -> str:
    f = _p(p, "frequency_hz", 512)
    temp = _clamp(_p(p, "temperature_c", 25), 0, 40)
    dia = _clamp(_p(p, "tube_diameter_cm", 3.0), 1.5, 6.0)
    v = 331 + 0.6 * temp
    l1 = v / (4 * f) - 0.3 * dia / 100
    frac = _clamp(l1 / 0.5, 0.05, 0.95)
    level = 228 - frac * 160
    measured = _num(r.get("measured"), v)
    return _frame(
        f"""
        <rect x="292" y="66" width="58" height="162" rx="6" fill="url(#glassG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="294" y="{level:.1f}" width="54" height="{228 - level:.1f}" rx="4" fill="rgba(56,189,248,.42)"/>
        <line x1="294" y1="{level:.1f}" x2="348" y2="{level:.1f}" stroke="#0284c7" stroke-width="2"/>
        <rect x="372" y="86" width="16" height="140" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="1.4"/>
        {_ticks(376, 90, 26, 6.2, 8)}
        <rect x="370" y="{level - 3:.1f}" width="20" height="6" rx="3" fill="#0f766e"/>
        <g class="hum">
        <path d="M296 54 q10 -14 20 0 q10 14 20 0" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <line x1="316" y1="54" x2="316" y2="40" stroke="{_DARK}" stroke-width="2"/>
        </g>
        <text x="316" y="34" text-anchor="middle" font-family="Inter,sans-serif" font-size="12" font-weight="600" fill="#334155">{f:.0f} Hz</text>
        <text x="398" y="{level - 8:.1f}" font-family="Inter,sans-serif" font-size="12" fill="#0f766e">L₁ = {l1 * 100:.1f} cm</text>
        {_tag(320, 84, f"v = {measured:.0f} m/s · end correction {0.3 * dia / 100 * 1000:.1f} mm")}
        """,
        "Resonance tube · the water level finds the loudest point",
    )


def _circuit_shell(component: str, needle: float = 0.0, flow: str = "flow") -> str:
    return textwrap.dedent(f"""
        <path d="M156 92 H546 V206 H156 Z" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <path d="M156 92 H546 V206 H156 Z" fill="none" stroke="#0ea5e9" stroke-width="2" stroke-dasharray="4 12" class="{flow}" opacity=".8"/>
        <rect x="148" y="174" width="18" height="36" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <line x1="157" y1="182" x2="157" y2="202" stroke="{_DARK}" stroke-width="3"/>
        <line x1="148" y1="192" x2="166" y2="192" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="256" cy="92" r="20" fill="#fff" stroke="{_DARK}" stroke-width="2.2"/>
        <text x="249" y="97" font-family="Inter,sans-serif" font-size="14" fill="#334155">A</text>
        <line x1="256" y1="92" x2="{256 + 13 * math.sin(math.radians(needle)):.1f}" y2="{92 - 13 * math.cos(math.radians(needle)):.1f}" stroke="#dc2626" stroke-width="2.2"/>
        <circle cx="330" cy="206" r="20" fill="#fff" stroke="{_DARK}" stroke-width="2.2"/>
        <text x="322" y="211" font-family="Inter,sans-serif" font-size="14" fill="#334155">V</text>
        {component}
    """).strip()


def _resistor(x: float, y: float, label: str) -> str:
    return (
        f'<path d="M{x} {y} l8 0 l7 -13 l12 26 l12 -26 l12 26 l7 -13 l8 0" fill="none" stroke="{_DARK}" stroke-width="2.4"/>'
        f'<text x="{x + 34:.1f}" y="{y - 18:.1f}" text-anchor="middle" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{label}</text>'
    )


def _ohm(p: dict, r: dict) -> str:
    resistance = _clamp(_p(p, "resistance_ohm", 10), 2, 50)
    volts = _clamp(_p(p, "max_voltage", 6), 1, 12)
    current = volts / resistance
    needle = _clamp(current / 2 * 50, 0, 50)
    flow = "flow" if current > 0.05 else "flow slow"
    return _frame(
        _circuit_shell(
            _resistor(430, 92, f"R = {resistance:.0f} Ω"),
            needle,
            flow,
        )
        + _tag(320, 74, f"V = {volts:.1f} V · I = {current:.2f} A"),
        "Ohm's law · raise the voltage and the ammeter needle and current flow respond",
    )


def _series(p: dict, r: dict) -> str:
    r1 = _clamp(_p(p, "r1", 10), 2, 50)
    r2 = _clamp(_p(p, "r2", 20), 2, 50)
    mode = p.get("mode", "series")
    if mode == "parallel":
        component = f"""
        <path d="M380 92 V60 H520 V92" fill="none" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M380 92 V124 H520 V92" fill="none" stroke="{_DARK}" stroke-width="2.2"/>
        {_resistor(408, 60, f"R₁ {r1:.0f} Ω")}
        {_resistor(408, 124, f"R₂ {r2:.0f} Ω")}
        """
    else:
        component = (
            _resistor(380, 92, f"R₁ {r1:.0f} Ω")
            + _resistor(470, 92, f"R₂ {r2:.0f} Ω")
        )
    req = _num(r.get("measured"), r1 + r2 if mode == "series" else r1 * r2 / (r1 + r2))
    return _frame(
        _circuit_shell(component, 20, "flow")
        + _tag(320, 74, f"{mode} · R_eq = {req:.1f} Ω"),
        "Series and parallel · switch the combination and the wiring redraws",
    )


def _spherometer(p: dict, r: dict) -> str:
    radius = _clamp(_p(p, "true_radius_mm", 100), 50, 300)
    legs = _clamp(_p(p, "leg_distance_mm", 50), 30, 60)
    sag = legs * legs / (6 * radius)
    sep = legs * 2.4
    drop = _clamp(sag * 7, 6, 38)
    return _frame(
        f"""
        <path d="M{320 - sep / 2 - 40:.1f} 200 Q320 {200 - drop * 4:.1f} {320 + sep / 2 + 40:.1f} 200"
              fill="none" stroke="#93c5fd" stroke-width="14" opacity=".75"/>
        <path d="M{320 - sep / 2 - 40:.1f} 200 Q320 {200 - drop * 4:.1f} {320 + sep / 2 + 40:.1f} 200"
              fill="none" stroke="{_DARK}" stroke-width="1.8"/>
        <line x1="{320 - sep / 2:.1f}" y1="132" x2="{320 - sep / 2:.1f}" y2="{200 - drop * .25:.1f}" stroke="{_DARK}" stroke-width="3"/>
        <line x1="{320 + sep / 2:.1f}" y1="132" x2="{320 + sep / 2:.1f}" y2="{200 - drop * .25:.1f}" stroke="{_DARK}" stroke-width="3"/>
        <rect x="286" y="112" width="68" height="18" rx="5" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="312" y="62" width="16" height="52" rx="5" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="320" cy="56" r="14" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <line x1="320" y1="124" x2="320" y2="{132 + drop:.1f}" stroke="{_DARK}" stroke-width="2.4"/>
        <circle cx="320" cy="{132 + drop:.1f}" r="4" fill="#0f766e"/>
        {_tag(320, 74, f"h = {sag:.2f} mm · legs {legs:.0f} mm")}
        <text x="452" y="150" font-family="Inter,sans-serif" font-size="12" fill="#475569">R = {radius:.0f} mm</text>
        """,
        "Spherometer · the centre screw rises with the sagitta of the surface",
    )


def _specific_heat(p: dict, r: dict) -> str:
    mass_solid = _clamp(_p(p, "mass_solid_g", 100), 50, 300)
    mass_water = _clamp(_p(p, "mass_water_g", 150), 100, 400)
    temp = _clamp(_p(p, "temp_solid_c", 100), 60, 100)
    metal = p.get("metal", "copper")
    colours = {
        "aluminium": "#d1d5db",
        "iron": "#64748b",
        "copper": "#c2410c",
        "lead": "#475569",
    }
    block = 20 + (mass_solid - 50) / 250 * 34
    water_h = 36 + (mass_water - 100) / 300 * 58
    water_top = 218 - water_h
    mix = _num(r.get("extras") and r["extras"][0][1], 30)
    return _frame(
        f"""
        <rect x="236" y="108" width="168" height="116" rx="14" fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="254" y="{water_top:.1f}" width="132" height="{218 - water_top:.1f}" rx="8" fill="rgba(56,189,248,.38)" stroke="{_DARK}" stroke-width="1.2"/>
        <rect x="{320 - block / 2:.1f}" y="{210 - block:.1f}" width="{block:.1f}" height="{block:.1f}" rx="3"
              fill="{colours.get(metal, '#c2410c')}" stroke="{_DARK}" stroke-width="1.8"/>
        <text x="320" y="{204 - block:.1f}" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="#334155">{mass_solid:.0f} g</text>
        {_thermometer(382, 210, 118, temp, 0, 110)}
        <rect x="234" y="100" width="172" height="14" rx="6" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        {_tag(320, 74, f"{metal} block {temp:.0f} °C → mix {mix:.1f} °C")}
        <text x="258" y="214" font-family="Inter,sans-serif" font-size="11" fill="#0f172a">water {mass_water:.0f} g</text>
        """,
        "Method of mixtures · block size, water volume and thermometer all respond",
    )


def _filament(p: dict, r: dict) -> str:
    rated = _clamp(_p(p, "rated_voltage", 12), 3, 12)
    bright = _clamp(rated / 12, 0.25, 1.0)
    resistance = _num(r.get("measured"), 30.6)
    glow_op = 0.08 + bright * 0.55
    filament = "#fbbf24" if bright > 0.5 else "#f97316"
    return _frame(
        f"""
        <path d="M156 92 H546 V206 H156 Z" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="148" y="174" width="18" height="36" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <line x1="157" y1="182" x2="157" y2="202" stroke="{_DARK}" stroke-width="3"/>
        <line x1="148" y1="192" x2="166" y2="192" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="330" cy="92" r="46" fill="#fef9c3" opacity="{glow_op:.2f}" class="glow"/>
        <circle cx="330" cy="92" r="34" fill="#fffbeb" stroke="{_DARK}" stroke-width="2"/>
        <path d="M312 108 l0 -10 l6 14 l7 -18 l7 18 l7 -18 l7 18 l6 -14 l0 10" fill="none" stroke="{filament}" stroke-width="2.4"/>
        <rect x="322" y="108" width="16" height="12" fill="url(#metalG)" stroke="{_DARK}" stroke-width="1.4"/>
        {_tag(320, 74, f"{rated:.0f} V · R = {resistance:.1f} Ω")}
        """,
        "Filament lamp · the bulb glows brighter as the rated voltage rises",
    )


def _rc(p: dict, r: dict) -> str:
    resistance = _clamp(_p(p, "resistance_kohm", 10), 1, 100)
    cap = _clamp(_p(p, "capacitance_uf", 100), 10, 1000)
    supply = _clamp(_p(p, "supply_voltage", 6), 1, 12)
    tau = resistance * cap / 1000
    charged = supply * 0.632
    fill = 22 + _clamp(supply / 12, 0, 1) * 48
    tau_px = 10 + _clamp(math.log10(max(tau, 0.01) * 100) / 3, 0, 1) * 62
    return _frame(
        f"""
        <path d="M156 92 H546 V206 H156 Z" fill="none" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="148" y="174" width="18" height="36" rx="3" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <line x1="157" y1="182" x2="157" y2="202" stroke="{_DARK}" stroke-width="3"/>
        <line x1="148" y1="192" x2="166" y2="192" stroke="{_DARK}" stroke-width="2"/>
        <line x1="452" y1="58" x2="452" y2="126" stroke="{_DARK}" stroke-width="5"/>
        <line x1="472" y1="58" x2="472" y2="126" stroke="{_DARK}" stroke-width="5"/>
        <text x="438" y="146" font-family="Inter,sans-serif" font-size="12" fill="#475569">C = {cap:.0f} µF</text>
        <path d="M496 92 h24" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="520" y="74" width="18" height="36" rx="3" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <text x="548" y="70" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">R</text>
        <rect x="330" y="64" width="20" height="86" rx="6" fill="#f8fafc" stroke="{_DARK}" stroke-width="1.8"/>
        <rect x="333" y="{150 - fill:.1f}" width="14" height="{fill:.1f}" rx="4" fill="#0ea5e9" opacity=".8"/>
        <text x="340" y="162" text-anchor="middle" font-family="Inter,sans-serif" font-size="10" fill="#475569">{supply:.1f} V</text>
        <rect x="382" y="64" width="12" height="86" rx="5" fill="#e2e8f0" stroke="{_DARK}" stroke-width="1.2"/>
        <rect x="384" y="{150 - tau_px:.1f}" width="8" height="{tau_px:.1f}" rx="4" fill="#0f766e"/>
        <text x="388" y="56" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="#0f766e">τ</text>
        {_tag(320, 74, f"τ = RC = {tau:.2f} s · {charged:.2f} V at 1τ")}
        """,
        "RC circuit · the time constant grows with R and C",
    )


# ------------------------------------------------------------------- chemistry
def _burette(cx: float, top: float, bottom: float, frac: float, colour: str, flask_colour: str) -> str:
    frac = _clamp(frac, 0.0, 1.0)
    level = top + frac * (bottom - top - 8)
    return textwrap.dedent(f"""
        <rect x="{cx - 10:.1f}" y="{top}" width="20" height="{bottom - top:.1f}" rx="4" fill="url(#glassG)" stroke="{_DARK}" stroke-width="1.8"/>
        <rect x="{cx - 8:.1f}" y="{level:.1f}" width="16" height="{bottom - level - 2:.1f}" rx="3" fill="{colour}" opacity=".85"/>
        <line x1="{cx - 8:.1f}" y1="{level:.1f}" x2="{cx + 8:.1f}" y2="{level:.1f}" stroke="#1e293b" stroke-width="1.6"/>
        <path d="M{cx - 3:.1f} {bottom} l-4 8 h8 z" fill="{colour}"/>
        <rect x="{cx + 18:.1f}" y="{top + 6}" width="9" height="{bottom - top - 18:.1f}" rx="2" fill="#f8fafc" stroke="{_DARK}" stroke-width="1"/>
        {_ticks(cx + 18, top + 12, 10, 0, 6)}
        <path d="M{cx - 62:.1f} {bottom + 66:.1f} L{cx - 62:.1f} {bottom + 26:.1f} L{cx - 18:.1f} {bottom + 8:.1f}
                 L{cx + 18:.1f} {bottom + 8:.1f} L{cx + 62:.1f} {bottom + 26:.1f} L{cx + 62:.1f} {bottom + 66:.1f}
                 Q{cx + 62:.1f} {bottom + 74:.1f} {cx + 52:.1f} {bottom + 74:.1f}
                 L{cx - 52:.1f} {bottom + 74:.1f} Q{cx - 62:.1f} {bottom + 74:.1f} {cx - 62:.1f} {bottom + 66:.1f} Z"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2"/>
        <path d="M{cx - 58:.1f} {bottom + 58:.1f} L{cx + 58:.1f} {bottom + 58:.1f} L{cx + 62:.1f} {bottom + 66:.1f}
                 Q{cx + 62:.1f} {bottom + 74:.1f} {cx + 52:.1f} {bottom + 74:.1f}
                 L{cx - 52:.1f} {bottom + 74:.1f} Q{cx - 62:.1f} {bottom + 74:.1f} {cx - 62:.1f} {bottom + 66:.1f} Z"
              fill="{flask_colour}"/>
    """).strip()


def _titration(p: dict, r: dict, purple: bool = False) -> str:
    titre = _num((r.get("extras") or [("", "0", "")])[0][1], 0)
    indicator = p.get("indicator", "phenolphthalein")
    flask = "rgba(236,72,153,.55)" if indicator == "phenolphthalein" else "rgba(251,191,36,.5)"
    colour = "rgba(168,85,247,.75)" if purple else "rgba(56,189,248,.7)"
    frac = _clamp(titre / 50, 0.02, 0.95)
    return _frame(
        _burette(320, 46, 148, frac, colour, flask)
        + _tag(320, 66, f"titre {titre:.2f} cm³ · {'KMnO₄' if purple else 'NaOH'}")
        + f'<text x="392" y="120" font-family="Inter,sans-serif" font-size="12" fill="#475569">{indicator}</text>',
        "Volumetric analysis · the burette empties and the flask turns at the end point",
    )


def _chromatography(p: dict, r: dict) -> str:
    solvent = p.get("solvent", "water-alcohol")
    front = {"water-alcohol": 0.74, "n-butanol": 0.56, "ethanol-ammonia": 0.66}.get(solvent, 0.7)
    plate_top = 64
    baseline = 172
    height = baseline - plate_top
    front_y = baseline - height * front
    obs = r.get("observation") or {}
    spots = [("#a855f7", 0.62), ("#f59e0b", 0.44), ("#38bdf8", 0.24)]
    dots = "".join(
        f'<circle cx="{330 + i * 9 - 9:.1f}" cy="{baseline - height * f:.1f}" r="5" fill="{c}" opacity=".9"/>'
        for i, (c, f) in enumerate(spots)
    )
    return _frame(
        f"""
        <path d="M244 108 L244 220 Q244 232 256 232 L400 232 Q412 232 412 220 L412 108"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M246 168 L246 220 Q246 230 256 230 L400 230 Q410 230 410 220 L410 168 Z" fill="rgba(56,189,248,.22)"/>
        <rect x="304" y="{plate_top}" width="56" height="{baseline - plate_top + 14}" rx="3" fill="#fffdf5" stroke="{_DARK}" stroke-width="1.5"/>
        <line x1="308" y1="{baseline}" x2="356" y2="{baseline}" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 3"/>
        <line x1="308" y1="{front_y:.1f}" x2="356" y2="{front_y:.1f}" stroke="#0f766e" stroke-width="1.4" stroke-dasharray="4 3"/>
        {dots}
        <text x="372" y="{front_y:.1f}" font-family="Inter,sans-serif" font-size="11.5" fill="#0f766e">solvent front</text>
        <text x="372" y="{baseline + 4}" font-family="Inter,sans-serif" font-size="11.5" fill="#64748b">baseline</text>
        {_tag(320, 74, f"{solvent} · {obs.get('value', 'spots')}")}
        """,
        "Paper chromatography · the solvent front climbs and the dyes separate",
    )


def _conductivity(p: dict, r: dict) -> str:
    extra = (r.get("extras") or [("", "0/3", "")])[0][1]
    n = int(_num(extra, 0))
    glow = 0.10 + n / 3 * 0.62
    bulb = "#fde047" if n >= 3 else ("#fef08a" if n == 2 else ("#e2e8f0" if n == 1 else "#cbd5e1"))
    bubbles = ""
    if n >= 2:
        bubbles = "".join(
            f'<circle class="bub b{i + 1}" cx="{304 + (i % 3) * 20:.1f}" cy="{196 - i * 8:.1f}" r="{3 + n * 0.4:.1f}" fill="#e0f2fe"/>'
            for i in range(5)
        )
    return _frame(
        f"""
        <path d="M244 108 L244 220 Q244 232 256 232 L400 232 Q412 232 412 220 L412 108"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M246 150 L246 220 Q246 230 256 230 L400 230 Q410 230 410 220 L410 150 Z" fill="rgba(56,189,248,.30)"/>
        <rect x="292" y="86" width="12" height="136" rx="3" fill="#475569"/>
        <rect x="352" y="86" width="12" height="136" rx="3" fill="#475569"/>
        <path d="M298 86 V54 H358 V86" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="328" cy="48" r="17" fill="{bulb}" opacity="{glow:.2f}" class="glow"/>
        <circle cx="328" cy="48" r="12" fill="{bulb}" stroke="{_DARK}" stroke-width="2"/>
        <line x1="324" y1="44" x2="332" y2="52" stroke="{_DARK}" stroke-width="1.6"/>
        <line x1="332" y1="44" x2="324" y2="52" stroke="{_DARK}" stroke-width="1.6"/>
        {bubbles}
        {_tag(320, 74, f"{p.get('solute', 'solution')} · bulb {n}/3")}
        """,
        "Conductivity · ionic solutions light the bulb and release gas at the electrodes",
    )


def _solubility(p: dict, r: dict) -> str:
    temp = _clamp(_p(p, "temperature_c", 40), 0, 100)
    value = _num(r.get("measured"), 34.5)
    crystals = int(_clamp(round(12 - value / 8), 0, 12))
    crystal_svg = "".join(
        f'<rect x="{268 + (i % 6) * 18:.1f}" y="{210 - (i // 6) * 6:.1f}" width="12" height="7" rx="2" '
        f'fill="#e2e8f0" stroke="#475569" stroke-width=".9"/>'
        for i in range(crystals)
    )
    return _frame(
        f"""
        <path d="M244 108 L244 220 Q244 232 256 232 L400 232 Q412 232 412 220 L412 108"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M246 146 L246 220 Q246 230 256 230 L400 230 Q410 230 410 220 L410 146 Z" fill="rgba(56,189,248,.30)"/>
        {crystal_svg}
        {_thermometer(366, 210, 88, temp, 0, 100)}
        <text x="378" y="82" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#475569">{temp:.0f} °C</text>
        {_tag(320, 74, f"solubility {value:.1f} g / 100 g water")}
        """,
        "Solubility · warmer solvent dissolves more solid and the crystals disappear",
    )


_PH_COLOURS = {
    "gastric juice": "#f97316",
    "lemon juice": "#f97316",
    "vinegar": "#fb923c",
    "orange juice": "#fbbf24",
    "black coffee": "#a3e635",
    "milk": "#84cc16",
    "pure water": "#22c55e",
    "baking soda": "#14b8a6",
    "soap solution": "#3b82f6",
    "caustic soda": "#7c3aed",
}


def _ph(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour") or _PH_COLOURS.get(p.get("substance", ""), "#22c55e")
    ph = _num(r.get("measured"), 7)
    marker_x = 220 + _clamp(ph / 14, 0, 1) * 200
    return _frame(
        f"""
        <rect x="120" y="60" width="400" height="16" rx="8" fill="url(#phScale)"/>
        <linearGradient id="phScale" x1="0" x2="1">
          <stop offset="0" stop-color="#dc2626"/><stop offset=".2" stop-color="#f97316"/>
          <stop offset=".4" stop-color="#facc15"/><stop offset=".55" stop-color="#22c55e"/>
          <stop offset=".75" stop-color="#3b82f6"/><stop offset="1" stop-color="#7c3aed"/>
        </linearGradient>
        <line x1="{marker_x:.1f}" y1="54" x2="{marker_x:.1f}" y2="82" stroke="#0f172a" stroke-width="2.4"/>
        <text x="{marker_x:.1f}" y="94" text-anchor="middle" font-family="Inter,sans-serif" font-size="11.5" font-weight="600" fill="#0f172a">pH {ph:.1f}</text>
        {_tube(320, 108, 226, 52, 132, colour)}
        <rect x="296" y="126" width="48" height="4" rx="2" fill="#ffffff" opacity=".55"/>
        {_tag(320, 252, f"{p.get('substance', 'solution')} · {obs.get('value', '')}", "#334155")}
        """,
        "Universal indicator · the liquid colour and the pH marker move together",
    )


def _flame_scene(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour", "#facc15")
    return _frame(
        f"""
        <rect x="288" y="176" width="64" height="52" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <rect x="310" y="146" width="20" height="34" fill="#94a3b8" stroke="{_DARK}" stroke-width="1.6"/>
        {_flame(320, 148, colour, 1.0)}
        <line x1="410" y1="110" x2="352" y2="150" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="351" cy="151" r="6" fill="none" stroke="{_DARK}" stroke-width="2"/>
        <text x="416" y="106" font-family="Inter,sans-serif" font-size="12" fill="#475569">nichrome loop</text>
        {_tag(320, 74, f"{p.get('ion', 'ion')} · {obs.get('value', '')}")}
        """,
        "Flame test · the flame takes the characteristic colour of the metal ion",
    )


def _halide(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour", "#f8fafc")
    return _frame(
        f"""
        {_tube(320, 94, 222, 54, 128, "rgba(226,232,240,.65)")}
        <path d="M295 186 L345 186 Q345 220 320 220 Q295 220 295 186 Z" fill="{colour}" opacity=".95"/>
        <path d="M295 186 L345 186" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 3"/>
        <line x1="286" y1="172" x2="354" y2="172" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 3"/>
        <text x="368" y="196" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{obs.get('value', '')}</text>
        {_tag(320, 74, f"{p.get('halide', 'halide')} + AgNO₃")}
        """,
        "Silver nitrate test · the precipitate colour identifies the halide",
    )


def _heat_neutralisation(p: dict, r: dict) -> str:
    rise = _num((r.get("extras") or [("", "0", "")])[1][1], 6.9)
    temp = 25 + rise
    measured = _num(r.get("measured"), -57.5)
    return _frame(
        f"""
        <rect x="236" y="108" width="168" height="116" rx="14" fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.4"/>
        <rect x="254" y="150" width="132" height="70" rx="8" fill="rgba(251,191,36,.35)" stroke="{_DARK}" stroke-width="1.2"/>
        {_thermometer(382, 210, 118, temp, 0, 60)}
        <rect x="234" y="100" width="172" height="14" rx="6" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <path d="M292 150 q28 -14 56 0" fill="none" stroke="#f97316" stroke-width="2" class="glow"/>
        {_tag(320, 74, f"ΔT = {rise:.2f} K · ΔH = {measured:.1f} kJ/mol")}
        <text x="250" y="92" font-family="Inter,sans-serif" font-size="11" fill="#7c2d12">HCl + NaOH</text>
        """,
        "Neutralisation · the thermometer climbs as the acid and alkali react",
    )


def _salt_analysis(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour", "#60a5fa")
    cation = p.get("cation", "copper")
    anion = p.get("anion", "chloride")
    return _frame(
        f"""
        {_tube(320, 88, 222, 58, 120, "rgba(226,232,240,.5)")}
        <path d="M292 176 L348 176 L348 204 Q348 220 320 220 Q292 220 292 204 Z" fill="{colour}" opacity=".9"/>
        <line x1="292" y1="176" x2="348" y2="176" stroke="#475569" stroke-width="1.1" stroke-dasharray="4 3"/>
        <rect x="296" y="130" width="48" height="34" rx="6" fill="rgba(255,255,255,.45)"/>
        <text x="320" y="152" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#334155">NaOH</text>
        <text x="384" y="170" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{obs.get('value', '')}</text>
        {_tag(320, 74, f"{cation} · {anion}")}
        """,
        "Salt analysis · the precipitate colour narrows down the cation",
    )


def _carbonyl(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour", "#e5e7eb")
    test = p.get("test", "tollens")
    sample = p.get("sample", "aldehyde")
    mirror = ""
    if test == "tollens" and sample == "aldehyde":
        mirror = (
            '<path d="M295 112 Q295 200 320 218 Q345 200 345 112" fill="none" '
            'stroke="#cbd5e1" stroke-width="9" opacity=".95"/>'
        )
    return _frame(
        f"""
        {_tube(320, 94, 222, 56, 132, colour)}
        {mirror}
        <text x="360" y="150" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{test}</text>
        {_tag(320, 74, f"{sample} · {obs.get('value', '')}")}
        """,
        "Carbonyl test · the tube shows a mirror, a red precipitate or no change",
    )


# --------------------------------------------------------------------- biology
def _sav(p: dict, r: dict) -> str:
    side = _clamp(_p(p, "size_cm", 2), 1, 4)
    px = 46 + (side - 1) * 34
    reached = _num((r.get("extras") or [("", "0", "")])[1][1], 88)
    core = px * math.sqrt(max(0.02, 1 - reached / 100))
    ratio = _num(r.get("measured"), 6 / side)
    return _frame(
        f"""
        <rect x="196" y="200" width="300" height="24" rx="5" fill="#f1f5f9" stroke="{_DARK}" stroke-width="2"/>
        <rect x="{320 - px / 2:.1f}" y="{218 - px:.1f}" width="{px:.1f}" height="{px:.1f}" rx="4" fill="#fcd34d" stroke="#92400e" stroke-width="2"/>
        <rect x="{320 - core / 2:.1f}" y="{218 - px + (px - core) / 2:.1f}" width="{core:.1f}" height="{core:.1f}" fill="#fef3c7" opacity=".95"/>
        <text x="{320 + px / 2 + 10:.1f}" y="{218 - px / 2:.1f}" font-family="Inter,sans-serif" font-size="12" fill="#475569">{side:.0f} cm</text>
        <text x="320" y="190" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#92400e">dye reached {reached:.0f}% of the volume</text>
        {_tag(320, 74, f"SA : V = {ratio:.2f} cm⁻¹")}
        """,
        "Surface area to volume · grow the cube and the stained shell shrinks",
    )


def _osmosis(p: dict, r: dict) -> str:
    conc = _clamp(_p(p, "sucrose_conc", 0.3), 0, 0.5)
    time = _clamp(_p(p, "time_min", 30), 10, 60)
    iso = _num((r.get("extras") or [("", "0.315", "")])[0][1], 0.315)
    factor = _clamp(1 + (iso - conc) * 1.6, 0.55, 1.35)
    strips = ""
    for i, x in enumerate((286, 320, 354)):
        h = 64 * factor
        strips += (
            f'<rect x="{x - 12}" y="{218 - h:.1f}" width="24" height="{h:.1f}" rx="10" '
            f'transform="rotate({(-6 + i * 6)} {x} {218 - h / 2:.1f})" '
            f'fill="#fcd34d" stroke="#92400e" stroke-width="1.5"/>'
        )
    return _frame(
        f"""
        <path d="M244 108 L244 220 Q244 232 256 232 L400 232 Q412 232 412 220 L412 108"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M246 150 L246 220 Q246 230 256 230 L400 230 Q410 230 410 220 L410 150 Z" fill="rgba(74,222,128,.25)"/>
        {strips}
        {_tag(320, 74, f"{conc:.2f} mol/dm³ · {time:.0f} min · ×{factor:.2f}")}
        <text x="426" y="176" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{'swollen' if factor > 1.02 else ('shrunken' if factor < .98 else 'no change')}</text>
        """,
        "Osmosis · the potato strips swell in water and shrink in strong sugar",
    )


def _enzyme(p: dict, r: dict, title: str) -> str:
    temp = _clamp(_p(p, "temperature_c", 37), 0, 70)
    rate = _num((r.get("extras") or [("", "0", ""), ("", "0", ""), ("", "0", "")])[-1][1], 50)
    rate = _clamp(rate, 0, 100)
    blue, amber = (30, 58, 138), (180, 83, 9)
    mix = tuple(int(blue[i] + (amber[i] - blue[i]) * rate / 100) for i in range(3))
    colour = f"rgb({mix[0]},{mix[1]},{mix[2]})"
    return _frame(
        f"""
        <path d="M232 96 L232 214 Q232 226 244 226 L396 226 Q408 226 408 214 L408 96"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M234 160 L234 214 Q234 224 244 224 L396 224 Q406 224 406 214 L406 160 Z" fill="rgba(56,189,248,.28)"/>
        {_thermometer(370, 206, 110, temp, 0, 80)}
        {_tube(300, 108, 208, 40, 138, colour)}
        <circle class="bub b1" cx="300" cy="196" r="3" fill="#e0f2fe"/>
        <circle class="bub b3" cx="310" cy="190" r="2.4" fill="#e0f2fe"/>
        {_tag(320, 74, f"{temp:.0f} °C · relative rate {rate:.0f}%")}
        """,
        title,
    )


def _photosynthesis(p: dict, r: dict) -> str:
    light = _clamp(_p(p, "light_intensity", 50), 0, 100)
    rate = _num((r.get("extras") or [("", "0", "")])[0][1], 47)
    n = int(_clamp(rate / 12, 0, 6))
    bubbles = "".join(
        f'<circle class="bub b{(i % 3) + 1}" cx="{318 + (i % 3) * 7 - 7:.1f}" cy="{168 - i * 10:.1f}" '
        f'r="{2.4 + (i % 2) * 0.8:.1f}" fill="#e0f2fe"/>'
        for i in range(n)
    )
    lamp_glow = 0.08 + light / 100 * 0.6
    return _frame(
        f"""
        <path d="M236 112 L236 210 Q236 222 248 222 L388 222 Q400 222 400 210 L400 112"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M238 146 L238 210 Q238 220 248 220 L388 220 Q398 220 398 210 L398 146 Z" fill="rgba(74,222,128,.26)"/>
        <path d="M318 214 q-22 -34 4 -64 q10 -14 4 -36" fill="none" stroke="#15803d" stroke-width="2.6"/>
        <g fill="#22c55e" opacity=".9">
          <ellipse cx="306" cy="170" rx="8" ry="4" transform="rotate(-30 306 170)"/>
          <ellipse cx="328" cy="150" rx="7" ry="4" transform="rotate(28 328 150)"/>
          <ellipse cx="314" cy="132" rx="6" ry="3.4" transform="rotate(-22 314 132)"/>
        </g>
        {bubbles}
        <rect x="470" y="70" width="6" height="126" fill="{_DARK}"/>
        <path d="M446 196 h54 l-10 16 h-34 z" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="473" cy="64" r="22" fill="#fef08a" opacity="{lamp_glow:.2f}" class="glow"/>
        <circle cx="473" cy="64" r="14" fill="#fef08a" stroke="{_DARK}" stroke-width="2"/>
        <text x="408" y="188" font-family="Inter,sans-serif" font-size="11" fill="#475569">lamp {light:.0f}%</text>
        {_tag(320, 74, f"{rate:.0f} bubbles / min")}
        """,
        "Photosynthesis · brighter light means a faster stream of oxygen bubbles",
    )


def _transpiration(p: dict, r: dict) -> str:
    rate = _num((r.get("extras") or [("", "0", "")][-1])[1] if r.get("extras") else 12, 12)
    heat = _clamp(rate / 20, 0, 1)
    paper = f"rgb({int(56 + 188 * heat)},{int(189 - 106 * heat)},{int(248 - 138 * heat)})"
    return _frame(
        f"""
        <path d="M180 168 Q246 74 386 96 Q416 156 336 202 Q250 232 180 168 Z"
              fill="rgba(74,222,128,.55)" stroke="#15803d" stroke-width="2.4"/>
        <path d="M188 166 Q268 156 348 112" fill="none" stroke="#166534" stroke-width="2"/>
        <rect x="252" y="150" width="22" height="22" rx="2" fill="{paper}" stroke="{_DARK}" stroke-width="1.2"/>
        <rect x="300" y="132" width="22" height="22" rx="2" fill="{paper}" stroke="{_DARK}" stroke-width="1.2"/>
        <text x="420" y="120" font-family="Inter,sans-serif" font-size="12" fill="#475569">cobalt chloride paper</text>
        <text x="420" y="142" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{p.get('condition', '')}</text>
        {_tag(320, 74, f"water loss {rate:.1f} g / 30 min")}
        """,
        "Transpiration · the paper turns from blue to pink faster in dry, moving air",
    )


def _respiration(p: dict, r: dict) -> str:
    rise = _num((r.get("extras") or [("", "0", "")])[0][1], 11)
    live = p.get("seed_type", "germinating seeds").startswith("germinating")
    t_live = 25 + (rise if live else 0.2)
    t_dead = 25.2
    return _frame(
        f"""
        <path d="M236 106 L236 160 L204 218 Q198 228 210 228 L330 228 Q342 228 336 218 L304 160 L304 106 Z"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M214 200 L326 200 L336 218 Q342 228 330 228 L210 228 Q198 228 204 218 Z" fill="rgba(74,222,128,.22)"/>
        <path d="M398 106 L398 160 L366 218 Q360 228 372 228 L492 228 Q504 228 498 218 L466 160 L466 106 Z"
              fill="url(#glassG)" stroke="{_DARK}" stroke-width="2.2"/>
        <path d="M376 200 L488 200 L498 218 Q504 228 492 228 L372 228 Q360 228 366 218 Z" fill="rgba(148,163,184,.22)"/>
        {_thermometer(258, 200, 96, t_live, 0, 45)}
        {_thermometer(420, 200, 96, t_dead, 0, 45)}
        <text x="258" y="88" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="#475569">{'germinating' if live else 'boiled'} {t_live:.1f} °C</text>
        <text x="420" y="88" text-anchor="middle" font-family="Inter,sans-serif" font-size="10.5" fill="#475569">control {t_dead:.1f} °C</text>
        {_tag(320, 74, f"temperature rise {rise:.1f} °C")}
        """,
        "Respiration · only the living seeds warm their flask",
    )


def _food_tests(p: dict, r: dict) -> str:
    obs = r.get("observation") or {}
    colour = obs.get("colour", "#b91c1c")
    return _frame(
        f"""
        {_tube(320, 94, 222, 56, 136, "rgba(226,232,240,.35)")}
        <path d="M293 188 L347 188 L347 206 Q347 220 320 220 Q293 220 293 206 Z" fill="{colour}" opacity=".92"/>
        <line x1="293" y1="188" x2="347" y2="188" stroke="#475569" stroke-width="1.1" stroke-dasharray="4 3"/>
        <text x="364" y="150" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{p.get('test', '')}</text>
        <text x="364" y="170" font-family="Inter,sans-serif" font-size="11.5" fill="#334155">{p.get('sample', '')}</text>
        {_tag(320, 74, obs.get("value", ""))}
        """,
        "Food tests · the reagent colour reports which molecule is present",
    )


def _microscope(p: dict, r: dict) -> str:
    obj = _clamp(_p(p, "objective", 40), 4, 100)
    eye = _clamp(_p(p, "eyepiece", 10), 10, 15)
    mag = int(obj * eye)
    field = 180 / obj
    radius = _clamp(field * 13, 12, 70)
    cells = ""
    for i in range(6):
        cx = 394 + math.cos(i * 1.7) * radius * 0.45
        cy = 150 + math.sin(i * 2.1) * radius * 0.4
        cells += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{max(3, radius * .22):.1f}" ry="{max(2, radius * .16):.1f}" fill="rgba(134,239,172,.75)" stroke="#15803d" stroke-width=".8"/>'
    return _frame(
        f"""
        <rect x="252" y="214" width="136" height="14" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <path d="M300 214 q0 -70 44 -86 q40 -14 44 34" fill="none" stroke="url(#metalG)" stroke-width="18"/>
        <path d="M300 214 q0 -70 44 -86 q40 -14 44 34" fill="none" stroke="{_DARK}" stroke-width="1.8" opacity=".5"/>
        <rect x="356" y="132" width="74" height="12" rx="4" fill="{_METAL}" stroke="{_DARK}" stroke-width="2"/>
        <rect x="382" y="68" width="26" height="28" rx="6" fill="url(#metalG)" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="394" cy="52" r="12" fill="#f8fafc" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="394" cy="52" r="5" fill="#bae6fd"/>
        <circle cx="394" cy="150" r="{radius:.1f}" fill="#f0fdf4" stroke="{_DARK}" stroke-width="2"/>
        <circle cx="394" cy="150" r="{radius:.1f}" fill="none" stroke="#0f766e" stroke-width="1.4" stroke-dasharray="4 3"/>
        {cells}
        <text x="{394 + radius + 8:.1f}" y="152" font-family="Inter,sans-serif" font-size="11" fill="#0f766e">field {field:.2f} mm</text>
        {_tag(320, 74, f"{obj:.0f}× × {eye:.0f}× = {mag}×")}
        """,
        "Microscope · higher power shrinks the field of view and enlarges the cells",
    )


def _histogram(p: dict, r: dict) -> str:
    n = int(_clamp(_p(p, "sample_size", 30), 10, 60))
    mean = _num((r.get("extras") or [("", "0", "")])[0][1], 163)
    heights = []
    for i in range(7):
        z = (i - 3) * 0.9
        heights.append(max(3, int(54 * n / 30 * math.exp(-z * z / 2))))
    bars = "".join(
        f'<rect x="{214 + i * 36}" y="{216 - h}" width="34" height="{h}" fill="#2c4bd8" opacity=".8" stroke="#fff" stroke-width="1.2"/>'
        for i, h in enumerate(heights)
    )
    return _frame(
        f"""
        <line x1="206" y1="216" x2="472" y2="216" stroke="{_DARK}" stroke-width="2.2"/>
        <line x1="206" y1="84" x2="206" y2="216" stroke="{_DARK}" stroke-width="2.2"/>
        {bars}
        <line x1="206" y1="112" x2="466" y2="112" stroke="#b45309" stroke-width="1.6" stroke-dasharray="5 4"/>
        <text x="474" y="108" font-family="Inter,sans-serif" font-size="11" fill="#b45309">mean {mean:.1f} cm</text>
        <text x="340" y="232" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#334155">height (cm) · n = {n}</text>
        {_tag(320, 74, f"n = {n} · histogram scales with the sample")}
        """,
        "Biostatistics · the distribution fills in as the sample grows",
    )


def _blood_pressure(p: dict, r: dict) -> str:
    bp = (r.get("extras") or [("", "120/80", "")])[0][1]
    try:
        sys_v, dia_v = [int(x) for x in str(bp).split("/")]
    except ValueError:
        sys_v, dia_v = 120, 80
    angle = _clamp((sys_v - 60) / 120 * 240 - 120, -120, 120)
    dia_angle = _clamp((dia_v - 60) / 120 * 240 - 120, -120, 120)
    return _frame(
        f"""
        <rect x="180" y="132" width="170" height="72" rx="28" fill="#fecaca" stroke="{_DARK}" stroke-width="2.2"/>
        <rect x="196" y="148" width="138" height="40" rx="18" fill="#fca5a5" opacity=".7"/>
        <path d="M350 162 q66 -10 78 44" fill="none" stroke="{_DARK}" stroke-width="3"/>
        <circle cx="466" cy="118" r="52" fill="#f8fafc" stroke="{_DARK}" stroke-width="2.4"/>
        <circle cx="466" cy="118" r="42" fill="#fff" stroke="#cbd5e1" stroke-width="1.4"/>
        <line x1="466" y1="118" x2="{466 + 30 * math.sin(math.radians(angle)):.1f}" y2="{118 - 30 * math.cos(math.radians(angle)):.1f}" stroke="#dc2626" stroke-width="3"/>
        <line x1="466" y1="118" x2="{466 + 24 * math.sin(math.radians(dia_angle)):.1f}" y2="{118 - 24 * math.cos(math.radians(dia_angle)):.1f}" stroke="#2563eb" stroke-width="2.4"/>
        <circle cx="466" cy="118" r="4" fill="{_DARK}"/>
        <text x="466" y="184" text-anchor="middle" font-family="Inter,sans-serif" font-size="11" fill="#475569">mmHg</text>
        <text x="214" y="124" font-family="Inter,sans-serif" font-size="11.5" fill="#475569">{p.get('condition', '')}</text>
        {_tag(320, 74, f"{bp} mmHg")}
        """,
        "Sphygmomanometer · the needle swings to the systolic and diastolic pressures",
    )


def _dice(p: dict, r: dict) -> str:
    n = int(_clamp(_p(p, "rolls", 40), 10, 120))
    tall = _num((r.get("extras") or [("", "0", "")])[0][1], 0)
    short = _num((r.get("extras") or [("", "0", ""), ("", "0", "")])[1][1], 0)
    ratio = tall / (tall + short) * 100 if tall + short else 75
    bar_w = 300 * _clamp(ratio / 100, 0, 1)

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
        <g transform="rotate(-8 260 160)">{die(208, 104, pips_a)}</g>
        <g transform="rotate(9 400 160)">{die(348, 104, pips_b)}</g>
        <rect x="220" y="238" width="300" height="18" rx="9" fill="#e2e8f0"/>
        <rect x="220" y="238" width="{bar_w:.1f}" height="18" rx="9" fill="#0f766e"/>
        <text x="220" y="272" font-family="Inter,sans-serif" font-size="11" fill="#f8fafc">{tall:.0f} tall</text>
        <text x="520" y="272" text-anchor="end" font-family="Inter,sans-serif" font-size="11" fill="#fde68a">{short:.0f} short</text>
        {_tag(320, 74, f"{n} throws · {ratio:.0f}% tall (expected 75%)")}
        """,
        "Monohybrid cross · the ratio approaches 3 : 1 as the throws increase",
    )


# ---------------------------------------------------------------------- lookup
_SCENES = {
    "phy-vernier-ix": _caliper,
    "phy-screw-gauge-ix": _screw_gauge,
    "phy-moments-ix": _balance,
    "phy-hooke-ix": _spring,
    "phy-pendulum-x": _pendulum,
    "phy-resonance-x": _resonance,
    "phy-ohm-x": _ohm,
    "phy-series-x": _series,
    "phy-spherometer-xi": _spherometer,
    "phy-specific-heat-xi": _specific_heat,
    "phy-filament-xii": _filament,
    "phy-rc-xii": _rc,
    "chem-chromatography-ix": _chromatography,
    "chem-conductivity-ix": _conductivity,
    "chem-solubility-ix": _solubility,
    "chem-ph-x": _ph,
    "chem-standardise-naoh-x": _titration,
    "chem-oxalic-x": _titration,
    "chem-flame-x": _flame_scene,
    "chem-halide-x": _halide,
    "chem-heat-neutralisation-xi": _heat_neutralisation,
    "chem-kmno4-xi": lambda p, r: _titration(p, r, purple=True),
    "chem-salt-analysis-xii": _salt_analysis,
    "chem-carbonyl-xii": _carbonyl,
    "bio-sav-ix": _sav,
    "bio-osmosis-ix": _osmosis,
    "bio-amylase-temp-ix": lambda p, r: _enzyme(p, r, "Enzyme activity · the iodine colour fades as digestion speeds up"),
    "bio-amylase-ph-ix": lambda p, r: _enzyme(p, r, "Enzyme activity · pH moves the active site away from its optimum"),
    "bio-photosynthesis-ix": _photosynthesis,
    "bio-transpiration-ix": _transpiration,
    "bio-respiration-heat-ix": _respiration,
    "bio-food-tests-xi": _food_tests,
    "bio-microscope-xi": _microscope,
    "bio-biostatistics-x": _histogram,
    "bio-blood-pressure-xi": _blood_pressure,
    "bio-genetics-dice-xii": _dice,
}


def scene(practical: dict, params: dict | None = None, result: dict | None = None) -> None:
    """Render the live apparatus stage for a practical."""
    builder = _SCENES.get(practical.get("id", ""))
    if builder is None:
        return
    st.markdown(builder(params or {}, result or {}), unsafe_allow_html=True)
