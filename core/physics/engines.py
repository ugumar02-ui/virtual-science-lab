"""Physics simulation engines.

Pure Python, no Streamlit imports, so the same maths can later power a
Flutter/desktop build. Every engine returns a dict with a ``kind`` of either
``quantitative`` (measured vs accepted) or ``qualitative`` (an observation).
"""

from __future__ import annotations

import math
import random

G = 9.81


# ---------------------------------------------------------------- measurement
def vernier(
    true_diameter_mm: float = 20.0,
    zero_error_mm: float = 0.0,
    least_count: float = 0.02,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    rows, vals = [], []
    for trial in range(1, 4):
        observed = true_diameter_mm + rng.gauss(0, least_count / 2)
        scale = round(observed / least_count) * least_count
        corrected = scale - zero_error_mm
        vals.append(corrected)
        rows.append(
            {
                "Trial": trial,
                "Main scale (mm)": round(math.floor(scale), 2),
                "Vernier division": int(round((scale - math.floor(scale)) / least_count)),
                "Total reading (mm)": round(scale, 2),
                "Zero-corrected (mm)": round(corrected, 2),
            }
        )
    d = sum(vals) / len(vals)
    notes = []
    if abs(zero_error_mm) > 0:
        notes.append(
            f"The instrument has a zero error of {zero_error_mm:+.2f} mm. "
            "Every reading must be corrected by subtracting it."
        )
    return {
        "kind": "quantitative",
        "measured": d,
        "accepted": true_diameter_mm,
        "table": rows,
        "series": [],
        "notes": notes,
        "extras": [
            ("Least count", f"{least_count:.2f}", "mm"),
            ("Cross-section area", f"{math.pi * (d / 10) ** 2 / 4:.3f}", "cm²"),
            ("Mean corrected diameter", f"{d:.2f}", "mm"),
        ],
    }


def screw_gauge(
    true_diameter_mm: float = 0.50,
    zero_error_mm: float = 0.0,
    pitch_mm: float = 0.5,
    divisions: int = 50,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    least_count = pitch_mm / divisions
    rows, vals = [], []
    for trial in range(1, 4):
        observed = true_diameter_mm + rng.gauss(0, least_count / 2)
        scale = round(observed / least_count) * least_count
        corrected = scale - zero_error_mm
        vals.append(corrected)
        rows.append(
            {
                "Trial": trial,
                "Main scale (mm)": round(math.floor(scale / pitch_mm) * pitch_mm, 2),
                "Circular scale division": int(
                    round((scale % pitch_mm) / least_count)
                ),
                "Total reading (mm)": round(scale, 3),
                "Zero-corrected (mm)": round(corrected, 3),
            }
        )
    d = sum(vals) / len(vals)
    volume = (4 / 3) * math.pi * (d / 20) ** 3  # cm³ (d in mm -> radius cm = d/20)
    return {
        "kind": "quantitative",
        "measured": d,
        "accepted": true_diameter_mm,
        "table": rows,
        "series": [],
        "notes": [
            f"Least count = pitch ÷ divisions = {pitch_mm} ÷ {divisions} = {least_count:.3f} mm."
        ],
        "extras": [
            ("Least count", f"{least_count:.3f}", "mm"),
            ("Volume of sphere", f"{volume:.4f}", "cm³"),
            ("Zero error", f"{zero_error_mm:+.2f}", "mm"),
        ],
    }


def spherometer(
    true_radius_mm: float = 100.0,
    leg_distance_mm: float = 50.0,
    least_count_mm: float = 0.01,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    l = leg_distance_mm
    h_true = l**2 / (6 * true_radius_mm) + true_radius_mm / 2 - math.sqrt(
        max(true_radius_mm**2 - (l / 2) ** 2, 0)
    )
    h_true = max(h_true, 0.01)
    rows, radii = [], []
    for trial in range(1, 4):
        h = max(h_true + rng.gauss(0, least_count_mm / 2), least_count_mm)
        r = l**2 / (6 * h) + h / 2
        radii.append(r)
        rows.append(
            {
                "Trial": trial,
                "Mean leg distance l (mm)": round(l, 2),
                "Sagitta h (mm)": round(h, 3),
                "R = l²/6h + h/2 (mm)": round(r, 2),
            }
        )
    r_mean = sum(radii) / len(radii)
    return {
        "kind": "quantitative",
        "measured": r_mean,
        "accepted": true_radius_mm,
        "table": rows,
        "series": [],
        "notes": ["R = l² / 6h + h / 2, where l is the mean distance between the three legs."],
        "extras": [("Least count", f"{least_count_mm:.2f}", "mm")],
    }


# ------------------------------------------------------------------ mechanics
def moments(
    known_weight_n: float = 2.0,
    distance_known_cm: float = 30.0,
    distance_unknown_cm: float = 20.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    true_w = known_weight_n * distance_known_cm / distance_unknown_cm
    rows, vals = [], []
    for trial in range(1, 4):
        w = true_w * (1 + rng.gauss(0, 0.01))
        vals.append(w)
        rows.append(
            {
                "Trial": trial,
                "Known weight W₁ (N)": known_weight_n,
                "Distance d₁ (cm)": distance_known_cm,
                "Distance d₂ (cm)": distance_unknown_cm,
                "Unknown weight W₂ (N)": round(w, 3),
            }
        )
    w_mean = sum(vals) / len(vals)
    return {
        "kind": "quantitative",
        "measured": w_mean,
        "accepted": true_w,
        "table": rows,
        "series": [],
        "notes": [
            "Principle of moments: W₁ × d₁ = W₂ × d₂. The metre rod is balanced, so the "
            "clockwise moment equals the anticlockwise moment."
        ],
        "extras": [
            ("Moment of known weight", f"{known_weight_n * distance_known_cm / 100:.2f}", "N·m"),
            ("Moment of unknown weight", f"{w_mean * distance_unknown_cm / 100:.2f}", "N·m"),
        ],
    }


def hooke(
    spring_constant: float = 25.0,
    max_mass_g: float = 300.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    masses = [50, 100, 150, 200, 250, max_mass_g]
    xs, ys, rows = [], [], []
    for m in masses:
        f = m / 1000 * G
        x = f / spring_constant * 100  # cm
        x_meas = x + rng.gauss(0, 0.05)
        xs.append(x_meas)
        ys.append(f)
        rows.append(
            {
                "Mass (g)": m,
                "Load F (N)": round(f, 3),
                "Extension x (cm)": round(x_meas, 2),
                "F / x (N/cm)": round(f / x_meas, 2) if x_meas else 0,
            }
        )
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    gradient = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )
    k_measured = gradient * 100  # N/m
    return {
        "kind": "quantitative",
        "measured": k_measured,
        "accepted": spring_constant,
        "table": rows,
        "series": [
            {"name": "Load against extension", "x": [round(x, 2) for x in xs], "y": ys, "mode": "lines+markers"},
        ],
        "x_label": "Extension x (cm)",
        "y_label": "Load F (N)",
        "notes": [
            "Hooke's law: F = kx. The gradient of the F–x graph is the spring constant k. "
            "Beyond the elastic limit the line would curve."
        ],
        "extras": [("Gradient", f"{gradient:.2f}", "N/cm")],
    }


def pendulum(
    length_cm: float = 100.0,
    amplitude_deg: float = 10.0,
    mass_g: float = 50.0,
    timing_error_s: float = 0.12,
    oscillations: int = 20,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    length_m = length_cm / 100
    theta = math.radians(amplitude_deg)
    correction = 1 + theta**2 / 16 + 11 * theta**4 / 3072
    period_true = 2 * math.pi * math.sqrt(length_m / G) * correction

    rows, g_vals = [], []
    for trial in range(1, 4):
        total = oscillations * period_true + rng.gauss(0, timing_error_s)
        total = max(total, 0.01)
        period = total / oscillations
        g = 4 * math.pi**2 * length_m / period**2
        g_vals.append(g)
        rows.append(
            {
                "Trial": trial,
                "Time for 20 oscillations (s)": round(total, 2),
                "Period T (s)": round(period, 3),
                "g (m/s²)": round(g, 2),
            }
        )
    measured = sum(g_vals) / len(g_vals)

    lengths = list(range(20, 151, 10))
    theory_x = [n / 100 for n in lengths]
    theory_y = [(2 * math.pi * math.sqrt(x / G) * correction) ** 2 for x in theory_x]

    notes = [
        f"The mass of the bob ({mass_g:.0f} g) does not appear in T = 2π√(L/g), "
        "so changing it does not change the period. Try it — the result will not move."
    ]
    if amplitude_deg > 15:
        notes.append(
            f"At {amplitude_deg:.0f}° the motion is no longer strictly simple harmonic, "
            "so the measured period is slightly longer than the formula predicts."
        )
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": G,
        "table": rows,
        "series": [
            {"name": "Theory: T² against L", "x": theory_x, "y": theory_y, "mode": "lines"},
            {
                "name": "Your measurement",
                "x": [length_m],
                "y": [rows[-1]["Period T (s)"] ** 2],
                "mode": "markers",
            },
        ],
        "x_label": "Length L (m)",
        "y_label": "T² (s²)",
        "notes": notes,
        "extras": [
            ("Period T", f"{rows[-1]['Period T (s)']:.3f}", "s"),
            ("Oscillations timed", f"{oscillations}", ""),
        ],
    }


def resonance_tube(
    frequency_hz: float = 512.0,
    temperature_c: float = 25.0,
    tube_diameter_cm: float = 3.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    v = 331.3 * math.sqrt(1 + temperature_c / 273.15)
    wavelength = v / frequency_hz
    end_correction = 0.3 * tube_diameter_cm / 100
    l1_true = wavelength / 4 - end_correction
    l2_true = 3 * wavelength / 4 - end_correction

    rows, speeds = [], []
    for trial in range(1, 4):
        l1 = l1_true + rng.gauss(0, 0.002)
        l2 = l2_true + rng.gauss(0, 0.002)
        lam = 2 * (l2 - l1)
        speed = frequency_hz * lam
        speeds.append(speed)
        rows.append(
            {
                "Trial": trial,
                "First resonance L₁ (m)": round(l1, 3),
                "Second resonance L₂ (m)": round(l2, 3),
                "λ = 2(L₂−L₁) (m)": round(lam, 3),
                "v = fλ (m/s)": round(speed, 1),
            }
        )
    measured = sum(speeds) / len(speeds)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": v,
        "table": rows,
        "series": [],
        "notes": [
            f"At {temperature_c:.0f} °C the accepted speed of sound is "
            f"{v:.1f} m/s (v = 331.3√(1 + T/273.15))."
        ],
        "extras": [("Wavelength", f"{wavelength:.3f}", "m"), ("End correction", f"{end_correction:.4f}", "m")],
    }


# ---------------------------------------------------------------- electricity
def ohm_law(
    resistance_ohm: float = 10.0,
    max_voltage: float = 6.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    voltages = [round(0.5 * i, 1) for i in range(1, int(max_voltage / 0.5) + 1)]
    xs, ys, rows = [], [], []
    for v in voltages:
        i = v / resistance_ohm * (1 + rng.gauss(0, 0.004))
        xs.append(v)
        ys.append(i)
        rows.append(
            {
                "Voltage V (V)": v,
                "Current I (A)": round(i, 4),
                "V / I (Ω)": round(v / i, 2),
            }
        )
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    gradient = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )
    r_measured = 1 / gradient
    return {
        "kind": "quantitative",
        "measured": r_measured,
        "accepted": resistance_ohm,
        "table": rows,
        "series": [
            {"name": "V against I", "x": xs, "y": [round(y, 4) for y in ys], "mode": "lines+markers"}
        ],
        "x_label": "Current I (A)",
        "y_label": "Voltage V (V)",
        "notes": [
            "The V–I graph is a straight line through the origin, so V ∝ I. "
            "The gradient is the resistance in ohms."
        ],
        "extras": [("Gradient", f"{gradient:.2f}", "V/A")],
    }


def series_parallel(
    r1: float = 10.0,
    r2: float = 20.0,
    mode: str = "series",
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    if mode == "series":
        true_req = r1 + r2
        note = "In series the same current flows through both resistors: R = R₁ + R₂."
    else:
        true_req = (r1 * r2) / (r1 + r2)
        note = "In parallel the p.d. across both resistors is the same: 1/R = 1/R₁ + 1/R₂."

    rows, vals = [], []
    for trial in range(1, 4):
        req = true_req * (1 + rng.gauss(0, 0.005))
        vals.append(req)
        rows.append(
            {
                "Trial": trial,
                "R₁ (Ω)": r1,
                "R₂ (Ω)": r2,
                "Equivalent R (Ω)": round(req, 2),
            }
        )
    measured = sum(vals) / len(vals)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": true_req,
        "table": rows,
        "series": [],
        "notes": [note],
        "extras": [
            ("R₁", f"{r1:.1f}", "Ω"),
            ("R₂", f"{r2:.1f}", "Ω"),
            ("Combination", mode, ""),
        ],
    }


METALS = {"aluminium": 900.0, "iron": 450.0, "copper": 380.0, "lead": 130.0}


def specific_heat(
    metal: str = "copper",
    mass_solid_g: float = 100.0,
    mass_water_g: float = 150.0,
    temp_solid_c: float = 100.0,
    temp_water_c: float = 25.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    true_c = METALS.get(metal, 380.0)
    c_water = 4.18  # J per gram per kelvin
    c_solid = true_c / 1000  # J per gram per kelvin
    teq = (mass_solid_g * c_solid * temp_solid_c + mass_water_g * c_water * temp_water_c) / (
        mass_solid_g * c_solid + mass_water_g * c_water
    )
    rows, vals = [], []
    for trial in range(1, 4):
        t = teq + rng.gauss(0, 0.1)
        c = (mass_water_g * c_water * (t - temp_water_c)) / (
            mass_solid_g * (temp_solid_c - t)
        )
        c *= 1000  # J/kg·K
        vals.append(c)
        rows.append(
            {
                "Trial": trial,
                "Final temperature (°C)": round(t, 2),
                "Specific heat (J/kg·K)": round(c, 1),
            }
        )
    measured = sum(vals) / len(vals)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": true_c,
        "table": rows,
        "series": [],
        "notes": [
            "Method of mixtures: heat lost by the hot solid = heat gained by the water. "
            "c = m_w c_w (T − T_w) / [m_s (T_s − T)]."
        ],
        "extras": [
            ("Equilibrium temperature", f"{teq:.2f}", "°C"),
            ("Mass of solid", f"{mass_solid_g:.0f}", "g"),
            ("Mass of water", f"{mass_water_g:.0f}", "g"),
        ],
    }


def filament_lamp(
    rated_voltage: float = 12.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    # Tungsten: R rises with temperature, so I ∝ V^0.55 rather than V.
    k = 0.10
    xs, ys, rows = [], [], []
    for i in range(1, 13):
        v = rated_voltage * i / 12
        current = k * v**0.55 * (1 + rng.gauss(0, 0.005))
        xs.append(round(v, 2))
        ys.append(round(current, 4))
        rows.append(
            {
                "Voltage V (V)": round(v, 2),
                "Current I (A)": round(current, 4),
                "R = V/I (Ω)": round(v / current, 2),
            }
        )
    r_at_rated = rated_voltage / (k * rated_voltage**0.55)
    return {
        "kind": "quantitative",
        "measured": r_at_rated,
        "accepted": r_at_rated,
        "table": rows,
        "series": [
            {"name": "Filament characteristic", "x": xs, "y": ys, "mode": "lines+markers"}
        ],
        "x_label": "Voltage V (V)",
        "y_label": "Current I (A)",
        "notes": [
            "The graph curves, so the filament is a non-ohmic conductor. As the "
            "temperature rises, resistance increases — this is why the lamp does not "
            "follow Ohm's law."
        ],
        "extras": [("Resistance at rated voltage", f"{r_at_rated:.1f}", "Ω")],
    }


def rc_circuit(
    resistance_kohm: float = 10.0,
    capacitance_uf: float = 100.0,
    supply_voltage: float = 6.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    tau_ms = resistance_kohm * capacitance_uf / 1000  # kΩ × µF = ms
    xs, ys, rows = [], [], []
    for i in range(0, 21):
        t = tau_ms * 3 * i / 20
        v = supply_voltage * (1 - math.exp(-t / tau_ms))
        v_meas = v + rng.gauss(0, 0.01)
        xs.append(round(t, 2))
        ys.append(round(v_meas, 3))
        if i in (5, 10, 15, 20):
            rows.append(
                {
                    "Time t (ms)": round(t, 2),
                    "Voltage across C (V)": round(v_meas, 3),
                }
            )
    # Student reads the time at which V reaches 63.2% of the supply
    t63 = tau_ms * (1 + rng.gauss(0, 0.01))
    measured = t63
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": tau_ms,
        "table": rows,
        "series": [
            {"name": "Charging curve", "x": xs, "y": ys, "mode": "lines"}
        ],
        "x_label": "Time t (ms)",
        "y_label": "Voltage V (V)",
        "notes": [
            "Time constant τ = RC. After one time constant the capacitor has reached "
            "63.2 % of the supply voltage."
        ],
        "extras": [
            ("Supply voltage", f"{supply_voltage:.1f}", "V"),
            ("63.2 % level", f"{0.632 * supply_voltage:.2f}", "V"),
        ],
    }
