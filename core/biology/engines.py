"""Biology simulation engines."""

from __future__ import annotations

import math
import random


def osmosis(
    sucrose_conc: float = 0.3,
    time_min: float = 30.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    # Potato tissue is roughly isotonic with 0.30 mol/dm³ sucrose.
    isotonic = 0.30
    rows, changes = [], []
    for c in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
        pct = (isotonic - c) * 60 * (time_min / 30)
        pct_meas = pct + rng.gauss(0, 0.4)
        changes.append((c, pct_meas))
        rows.append(
            {
                "Sucrose conc. (mol/dm³)": c,
                "Initial mass (g)": 5.00,
                "Final mass (g)": round(5 * (1 + pct_meas / 100), 3),
                "Change in mass (%)": round(pct_meas, 2),
            }
        )
    measured = isotonic + rng.gauss(0, 0.008)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": isotonic,
        "table": rows,
        "series": [
            {
                "name": "Change in mass against concentration",
                "x": [c for c, _ in changes],
                "y": [round(p, 2) for _, p in changes],
                "mode": "lines+markers",
            }
        ],
        "x_label": "Sucrose concentration (mol/dm³)",
        "y_label": "Change in mass (%)",
        "notes": [
            "Where the graph crosses zero the solution is isotonic to the potato: water "
            "enters and leaves at the same rate. In dilute solutions the cells gain water "
            "and become turgid; in concentrated solutions they lose water and become "
            "flaccid (plasmolysis)."
        ],
        "extras": [
            ("Isotonic concentration", f"{measured:.3f}", "mol/dm³"),
            ("Immersion time", f"{time_min:.0f}", "min"),
        ],
    }


def enzyme(
    temperature_c: float = 37.0,
    ph: float = 7.0,
    substrate_conc: float = 1.0,
    enzyme_name: str = "amylase",
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    if enzyme_name == "pepsin":
        opt_temp, opt_ph, temp_sigma, ph_sigma = 37.0, 2.0, 10.0, 0.8
        substrate = "protein"
    else:
        opt_temp, opt_ph, temp_sigma, ph_sigma = 40.0, 7.0, 11.0, 1.1
        substrate = "starch"

    temp_factor = math.exp(-((temperature_c - opt_temp) ** 2) / (2 * temp_sigma**2))
    ph_factor = math.exp(-((ph - opt_ph) ** 2) / (2 * ph_sigma**2))
    denature = math.exp(-(temperature_c - 55) / 6.0) if temperature_c > 55 else 1.0
    sat = substrate_conc / (0.5 + substrate_conc)
    rate = max(100.0 * temp_factor * ph_factor * denature * sat, 0.01)
    time_s = 600.0 / rate

    measured = round(time_s * (1 + rng.gauss(0, 0.03)), 1)
    accepted = round(time_s, 1)

    xs = [t / 2 for t in range(0, 141)]
    ys = [
        100.0
        * math.exp(-((t - opt_temp) ** 2) / (2 * temp_sigma**2))
        * ph_factor
        * (math.exp(-(t - 55) / 6.0) if t > 55 else 1.0)
        * sat
        for t in xs
    ]

    notes = []
    if temperature_c >= 60:
        notes.append(
            f"At {temperature_c:.0f} °C the enzyme has denatured. The active site loses "
            "its shape permanently, so activity does not return on cooling."
        )
    elif temperature_c < 10:
        notes.append(
            "At low temperature the enzyme is inactive but not denatured — activity "
            "returns on warming, because molecules simply collide less often."
        )
    if abs(ph - opt_ph) > 1.5:
        notes.append(
            "A pH away from the optimum alters the charges on the active site, so the "
            f"{substrate} no longer fits."
        )

    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": accepted,
        "table": [
            {
                "Temperature (°C)": round(temperature_c, 1),
                "pH": round(ph, 1),
                "Relative rate (%)": round(rate, 1),
                f"Time for {substrate} to be digested (s)": measured,
            }
        ],
        "series": [
            {"name": "Activity against temperature", "x": [round(x, 1) for x in xs], "y": [round(y, 1) for y in ys], "mode": "lines"},
            {"name": "Your reading", "x": [temperature_c], "y": [round(rate, 1)], "mode": "markers"},
        ],
        "x_label": "Temperature (°C)",
        "y_label": "Relative enzyme activity (%)",
        "notes": notes,
        "extras": [
            ("Optimum temperature", f"{opt_temp:.0f}", "°C"),
            ("Optimum pH", f"{opt_ph:.1f}", ""),
            ("Relative rate", f"{rate:.1f}", "%"),
        ],
    }


def food_test(test: str = "benedict", sample: str = "glucose solution", seed: int | None = None) -> dict:
    data = {
        "benedict": {
            "glucose solution": ("brick-red precipitate", "#b91c1c", "reducing sugar present"),
            "bread": ("brick-red precipitate", "#b91c1c", "reducing sugar present"),
            "orange juice": ("brick-red precipitate", "#b91c1c", "reducing sugar present"),
            "water": ("stays blue", "#3b82f6", "no reducing sugar"),
        },
        "iodine": {
            "potato": ("blue-black", "#1e1b4b", "starch present"),
            "bread": ("blue-black", "#1e1b4b", "starch present"),
            "glucose solution": ("stays yellow-brown", "#d97706", "no starch"),
            "water": ("stays yellow-brown", "#d97706", "no starch"),
        },
        "biuret": {
            "egg albumin": ("violet / purple", "#7c3aed", "protein present"),
            "milk": ("violet / purple", "#7c3aed", "protein present"),
            "water": ("stays blue", "#3b82f6", "no protein"),
        },
        "emulsion": {
            "coconut oil": ("milky-white emulsion", "#f8fafc", "lipid present"),
            "peanuts": ("milky-white emulsion", "#f8fafc", "lipid present"),
            "water": ("clear", "#e5e7eb", "no lipid"),
        },
    }
    names = {
        "benedict": "Benedict's test for reducing sugar",
        "iodine": "Iodine test for starch",
        "biuret": "Biuret test for protein",
        "emulsion": "Emulsion test for lipid",
    }
    result, colour, conclusion = data[test][sample]
    return {
        "kind": "qualitative",
        "table": [{"Test": names[test], "Sample": sample.title(), "Result": result, "Conclusion": conclusion}],
        "series": [],
        "notes": [
            "Benedict's test must be heated in a water bath. The biuret test needs dilute "
            "copper sulphate and sodium hydroxide. The emulsion test uses ethanol followed "
            "by water."
        ],
        "extras": [("Conclusion", conclusion, "")],
        "observation": {"label": result, "colour": colour, "value": conclusion},
    }


def photosynthesis(
    light_intensity: float = 50.0,
    co2_percent: float = 1.0,
    temperature_c: float = 25.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    light_factor = light_intensity / (light_intensity + 25)
    co2_factor = co2_percent / (co2_percent + 0.5)
    temp_factor = math.exp(-((temperature_c - 30) ** 2) / (2 * 10**2))
    rate = 120 * light_factor * co2_factor * temp_factor
    rate = max(rate, 0.1)

    xs = list(range(0, 101, 5))
    ys = [
        round(120 * (x / (x + 25)) * co2_factor * temp_factor, 1) for x in xs
    ]
    measured = round(rate * (1 + rng.gauss(0, 0.02)), 1)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": round(rate, 1),
        "table": [
            {
                "Light intensity (arb.)": light_intensity,
                "CO₂ (%)": co2_percent,
                "Temperature (°C)": temperature_c,
                "Bubbles per minute": measured,
            }
        ],
        "series": [
            {"name": "Rate against light intensity", "x": xs, "y": ys, "mode": "lines"},
            {"name": "Your reading", "x": [light_intensity], "y": [measured], "mode": "markers"},
        ],
        "x_label": "Light intensity (arbitrary units)",
        "y_label": "Oxygen bubbles per minute",
        "notes": [
            "The rate rises with light intensity and then levels off: something else "
            "(CO₂ concentration or temperature) becomes the limiting factor."
        ],
        "extras": [("Rate", f"{measured:.1f}", "bubbles/min")],
    }


def transpiration(
    condition: str = "still air, bright light",
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    factors = {
        "still air, bright light": 1.0,
        "moving air (fan), bright light": 1.6,
        "still air, dark": 0.35,
        "humid air": 0.5,
        "warm, dry, moving air": 2.1,
    }
    base = 12.0
    rate = base * factors[condition] * (1 + rng.gauss(0, 0.02))
    xs = [0, 5, 10, 15, 20, 25, 30]
    ys = [round(rate * t / 30, 1) for t in xs]
    return {
        "kind": "quantitative",
        "measured": round(rate, 1),
        "accepted": round(base * factors[condition], 1),
        "table": [{"Condition": condition, "Water lost (g per 30 min)": round(rate, 1)}],
        "series": [
            {"name": "Water lost over time", "x": xs, "y": ys, "mode": "lines+markers"}
        ],
        "x_label": "Time (min)",
        "y_label": "Mass lost (g)",
        "notes": [
            "Transpiration is fastest when the air is warm, dry and moving: a steep "
            "water-potential gradient between the leaf and the air drives evaporation "
            "from the stomata."
        ],
        "extras": [("Condition", condition, ""), ("Rate", f"{rate:.1f}", "g/30 min")],
    }


def sav_ratio(size_cm: float = 2.0, seed: int | None = None) -> dict:
    rows = []
    for s in [1, 2, 3, 4]:
        sa = 6 * s**2
        vol = s**3
        rows.append(
            {
                "Cube side (cm)": s,
                "Surface area (cm²)": sa,
                "Volume (cm³)": vol,
                "SA : V ratio": round(sa / vol, 2),
            }
        )
    sa = 6 * size_cm**2
    vol = size_cm**3
    ratio = sa / vol
    # diffusion into a cube: only the outer shell absorbs dye
    depth = 0.5
    inner = max(size_cm - 2 * depth, 0)
    absorbed = (vol - inner**3) / vol * 100
    return {
        "kind": "quantitative",
        "measured": ratio,
        "accepted": ratio,
        "table": rows,
        "series": [
            {"name": "SA:V against size", "x": [1, 2, 3, 4], "y": [6.0, 3.0, 2.0, 1.5], "mode": "lines+markers"}
        ],
        "x_label": "Cube side (cm)",
        "y_label": "Surface area : volume ratio",
        "notes": [
            f"With a {size_cm:.0f} cm cube, dye reaches {absorbed:.0f} % of the volume in "
            "the same time. Smaller cubes have a larger surface-area-to-volume ratio, so "
            "diffusion supplies the whole cell — which is why cells stay small."
        ],
        "extras": [
            ("SA : V ratio", f"{ratio:.2f}", "cm⁻¹"),
            ("Volume reached by dye", f"{absorbed:.0f}", "%"),
        ],
    }


def respiration_heat(seed_type: str = "germinating seeds", seed: int | None = None) -> dict:
    rng = random.Random(seed)
    rate = 0.55 if seed_type == "germinating seeds" else 0.04
    rows, temps = [], []
    for t in [0, 5, 10, 15, 20]:
        temp = 25 + rate * t * (1 + rng.gauss(0, 0.02))
        temps.append(round(temp, 2))
        rows.append({"Time (min)": t, "Temperature (°C)": round(temp, 2)})
    rise = temps[-1] - 25
    return {
        "kind": "quantitative",
        "measured": round(rise, 2),
        "accepted": round(rate * 20, 2),
        "table": rows,
        "series": [
            {"name": "Temperature against time", "x": [0, 5, 10, 15, 20], "y": temps, "mode": "lines+markers"}
        ],
        "x_label": "Time (min)",
        "y_label": "Temperature (°C)",
        "notes": [
            "Germinating seeds respire aerobically and release heat. Boiled seeds have "
            "no living cells, so their temperature stays close to room temperature — "
            "this is the control."
        ],
        "extras": [("Temperature rise", f"{rise:.2f}", "°C"), ("Seeds", seed_type, "")],
    }


def magnification(objective: float = 40.0, eyepiece: float = 10.0, seed: int | None = None) -> dict:
    total = objective * eyepiece
    field_mm = 180 / objective if objective else 0
    return {
        "kind": "quantitative",
        "measured": total,
        "accepted": total,
        "table": [
            {
                "Objective lens": f"{objective:.0f}×",
                "Eyepiece": f"{eyepiece:.0f}×",
                "Total magnification": f"{total:.0f}×",
                "Field of view (mm)": round(field_mm, 2),
            }
        ],
        "series": [],
        "notes": [
            "Total magnification = objective × eyepiece. As magnification increases, the "
            "field of view gets smaller and the image gets dimmer."
        ],
        "extras": [("Total magnification", f"{total:.0f}", "×"), ("Field diameter", f"{field_mm:.2f}", "mm")],
    }


def biostatistics(sample_size: int = 30, seed: int | None = None) -> dict:
    """Mean, median and mode of a sample of heights."""
    import statistics

    rng = random.Random(seed)
    sample_size = int(sample_size)
    data = [max(140, min(195, round(rng.gauss(165, 9)))) for _ in range(sample_size)]
    mean = statistics.mean(data)
    median = statistics.median(data)
    mode = statistics.mode(data)
    sd = statistics.pstdev(data)

    bins = list(range(140, 196, 5))
    counts = [sum(1 for h in data if lo <= h < lo + 5) for lo in bins[:-1]]
    centres = [lo + 2.5 for lo in bins[:-1]]

    return {
        "kind": "quantitative",
        "measured": mean,
        "accepted": 165.0,
        "table": [{"Statistic": "Mean", "Value (cm)": round(mean, 2)},
                  {"Statistic": "Median", "Value (cm)": round(median, 2)},
                  {"Statistic": "Mode", "Value (cm)": mode},
                  {"Statistic": "Standard deviation", "Value (cm)": round(sd, 2)}],
        "series": [
            {"name": "Height distribution", "x": centres, "y": counts, "mode": "markers", "type": "bar"}
        ],
        "x_label": "Height (cm)",
        "y_label": "Number of students",
        "notes": [
            "The mean, median and mode are measures of central tendency. For a roughly "
            "symmetrical distribution they are close together; a large gap between mean "
            "and median suggests the data is skewed."
        ],
        "extras": [
            ("Mean", f"{mean:.1f}", "cm"),
            ("Median", f"{median:.1f}", "cm"),
            ("Mode", f"{mode}", "cm"),
        ],
    }


def blood_pressure(condition: str = "resting", seed: int | None = None) -> dict:
    rng = random.Random(seed)
    data = {
        "resting": (120, 80),
        "during sleep": (105, 65),
        "after exercise": (150, 90),
        "after caffeine": (130, 85),
    }
    systolic, diastolic = data[condition]
    sys_meas = round(systolic + rng.gauss(0, 2))
    dia_meas = round(diastolic + rng.gauss(0, 2))
    return {
        "kind": "quantitative",
        "measured": float(sys_meas),
        "accepted": float(systolic),
        "table": [
            {
                "Condition": condition,
                "Systolic (mmHg)": sys_meas,
                "Diastolic (mmHg)": dia_meas,
                "Pulse pressure (mmHg)": sys_meas - dia_meas,
            }
        ],
        "series": [],
        "notes": [
            "Blood pressure is written as systolic/diastolic, for example 120/80 mmHg. "
            "Systolic pressure is the peak during ventricular contraction; diastolic is "
            "the lowest pressure between beats. Exercise raises both."
        ],
        "extras": [
            ("Blood pressure", f"{sys_meas}/{dia_meas}", "mmHg"),
            ("Pulse pressure", f"{sys_meas - dia_meas}", "mmHg"),
        ],
    }
