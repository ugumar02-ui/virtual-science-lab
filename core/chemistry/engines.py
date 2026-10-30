"""Chemistry simulation engines."""

from __future__ import annotations

import math
import random

INDICATORS = {
    "phenolphthalein": {"low": 8.2, "high": 10.0, "acid": "#f4f4f5", "base": "#e0218a"},
    "methyl orange": {"low": 3.1, "high": 4.4, "acid": "#ef4444", "base": "#fbbf24"},
}

# Universal indicator colour scale
_PH_COLOURS = [
    (0, "#dc2626"),
    (2, "#f97316"),
    (4, "#facc15"),
    (6, "#a3e635"),
    (7, "#22c55e"),
    (8, "#14b8a6"),
    (10, "#3b82f6"),
    (12, "#6366f1"),
    (14, "#7c3aed"),
]


def ph_colour(ph: float) -> str:
    ph = max(0, min(14, ph))
    for (p1, c1), (p2, c2) in zip(_PH_COLOURS, _PH_COLOURS[1:]):
        if p1 <= ph <= p2:
            f = (ph - p1) / (p2 - p1)
            a = tuple(int(c1[i : i + 2], 16) for i in (1, 3, 5))
            b = tuple(int(c2[i : i + 2], 16) for i in (1, 3, 5))
            mix = tuple(round(a[i] + (b[i] - a[i]) * f) for i in range(3))
            return "#{:02x}{:02x}{:02x}".format(*mix)
    return _PH_COLOURS[-1][1]


def _ph_strong(ca: float, va: float, cb: float, vb: float) -> float:
    total = va + vb
    excess = ca * va - cb * vb
    if abs(excess) < 1e-12:
        return 7.0
    if excess > 0:
        return -math.log10(excess / total)
    return 14 + math.log10(-excess / total)


def _ph_weak(ca: float, va: float, cb: float, vb: float, ka: float) -> float:
    total = va + vb
    n_acid = ca * va
    n_base = cb * vb
    n_salt = n_base
    if n_base <= 1e-12:
        return -math.log10(math.sqrt(ka * ca))
    if n_acid > n_base:
        ratio = (n_acid - n_base) / n_salt
        return -math.log10(ka) + math.log10(max(ratio, 1e-9))
    if abs(n_acid - n_base) < 1e-9:
        c_salt = n_salt / total
        return 7 + 0.5 * -math.log10(ka) + 0.5 * math.log10(max(c_salt, 1e-9))
    return 14 + math.log10(max((n_base - n_acid) / total, 1e-12))


def titration(
    acid_conc: float = 0.10,
    acid_volume: float = 25.0,
    base_conc: float = 0.10,
    acid_type: str = "strong",
    n_factor: int = 1,
    indicator: str = "phenolphthalein",
    drop_error_ml: float = 0.05,
    seed: int | None = None,
) -> dict:
    """n_factor = moles of base per mole of acid (1 for HCl, 2 for oxalic acid)."""
    rng = random.Random(seed)
    ka = 1.8e-5 if acid_type == "weak" else None
    if ka:
        ph_fn = lambda v: _ph_weak(acid_conc, acid_volume, base_conc, v, ka)  # noqa: E731
    else:
        ph_fn = lambda v: _ph_strong(acid_conc, acid_volume, base_conc, v)  # noqa: E731

    v_eq = n_factor * acid_conc * acid_volume / base_conc

    steps = 400
    max_v = max(v_eq * 2, v_eq + 5)
    curve_x = [max_v * i / steps for i in range(steps + 1)]
    curve_y = [ph_fn(v) for v in curve_x]

    rows, volumes = [], []
    for trial in range(1, 4):
        endpoint = max(v_eq + rng.gauss(0, drop_error_ml), 0.0)
        volumes.append(endpoint)
        initial = round(rng.uniform(0.0, 0.5), 2)
        final = round(initial + endpoint, 2)
        rows.append(
            {
                "Trial": trial,
                "Initial reading (cm³)": initial,
                "Final reading (cm³)": final,
                "Volume of base used (cm³)": round(final - initial, 2),
            }
        )

    mean_v = sum(volumes) / len(volumes)
    measured = base_conc * mean_v / (n_factor * acid_volume)
    ind = INDICATORS[indicator]

    notes = []
    if acid_type == "weak" and indicator == "methyl orange":
        notes.append(
            "Methyl orange changes colour in acidic solution, far from the equivalence "
            "point of a weak acid titration, so the endpoint is read too early."
        )
    if n_factor == 2:
        notes.append(
            "Oxalic acid is diprotic: one mole of acid reacts with two moles of NaOH, "
            "so V_eq = 2·c(acid)·V(acid) / c(base)."
        )

    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": acid_conc,
        "unit": "mol/dm³",
        "table": rows,
        "series": [
            {"name": "Titration curve", "x": [round(v, 2) for v in curve_x], "y": [round(p, 2) for p in curve_y], "mode": "lines"},
            {"name": "Endpoint", "x": [round(mean_v, 2)], "y": [round(ph_fn(mean_v), 2)], "mode": "markers"},
        ],
        "x_label": "Volume of base added (cm³)",
        "y_label": "pH",
        "notes": notes,
        "extras": [
            ("Mean titre", f"{mean_v:.2f}", "cm³"),
            ("Equivalence volume", f"{v_eq:.2f}", "cm³"),
            ("Indicator range", f"{ind['low']}–{ind['high']}", ""),
        ],
    }


def ph_solutions(substance: str = "lemon juice", seed: int | None = None) -> dict:
    rng = random.Random(seed)
    table_data = {
        "gastric juice": (1.5, "strongly acidic"),
        "lemon juice": (2.2, "acidic"),
        "vinegar": (2.9, "acidic"),
        "orange juice": (3.8, "acidic"),
        "black coffee": (5.0, "weakly acidic"),
        "milk": (6.5, "slightly acidic"),
        "pure water": (7.0, "neutral"),
        "baking soda": (8.4, "weakly basic"),
        "soap solution": (10.5, "basic"),
        "caustic soda": (13.0, "strongly basic"),
    }
    ph_true, nature = table_data[substance]
    ph = round(ph_true + rng.gauss(0, 0.05), 2)
    return {
        "kind": "quantitative",
        "measured": ph,
        "accepted": ph_true,
        "table": [
            {"Substance": substance, "pH (universal indicator)": ph, "Nature": nature}
        ],
        "series": [],
        "notes": [
            f"{substance.title()} is {nature}. pH 7 is neutral; below 7 is acidic and "
            "above 7 is basic. Each unit on the pH scale is a tenfold change in [H⁺]."
        ],
        "extras": [("Indicator colour", ph_colour(ph), ""), ("Nature", nature, "")],
        "observation": {"label": "Universal indicator colour", "colour": ph_colour(ph), "value": f"pH {ph}"},
    }


def flame_test(ion: str = "sodium", seed: int | None = None) -> dict:
    table_data = {
        "sodium": ("golden yellow", "#facc15"),
        "potassium": ("lilac", "#c084fc"),
        "calcium": ("brick red", "#dc2626"),
        "strontium": ("crimson red", "#e11d48"),
        "barium": ("apple green", "#84cc16"),
        "copper": ("blue-green", "#22d3ee"),
        "lithium": ("carmine red", "#be123c"),
    }
    colour_name, hex_code = table_data[ion]
    return {
        "kind": "qualitative",
        "table": [{"Ion": ion.title(), "Flame colour": colour_name}],
        "series": [],
        "notes": [
            "The heat of the flame excites electrons to higher energy levels. As they "
            "fall back, they emit light of a characteristic wavelength — the flame colour."
        ],
        "extras": [("Observed colour", colour_name, "")],
        "observation": {"label": "Flame colour", "colour": hex_code, "value": colour_name},
    }


def halide_test(halide: str = "chloride", seed: int | None = None) -> dict:
    table_data = {
        "chloride": ("white precipitate", "#f8fafc", "soluble in dilute NH₄OH"),
        "bromide": ("cream precipitate", "#fef3c7", "soluble in concentrated NH₄OH"),
        "iodide": ("yellow precipitate", "#fde047", "insoluble in NH₄OH"),
    }
    colour_name, hex_code, solubility = table_data[halide]
    return {
        "kind": "qualitative",
        "table": [
            {
                "Halide": halide.title(),
                "Observation with AgNO₃": colour_name,
                "Solubility in NH₄OH": solubility,
            }
        ],
        "series": [],
        "notes": [
            "Silver nitrate gives a precipitate of the silver halide. The colour and the "
            "solubility in ammonia distinguish chloride, bromide and iodide."
        ],
        "extras": [("Precipitate", colour_name, "")],
        "observation": {"label": "Precipitate colour", "colour": hex_code, "value": colour_name},
    }


def conductivity(solute: str = "sodium chloride", seed: int | None = None) -> dict:
    table_data = {
        "distilled water": (0, "does not light", "no ions"),
        "sugar solution": (0, "does not light", "molecules, no ions"),
        "vinegar": (1, "dims", "weak acid, few ions"),
        "sodium chloride": (3, "bright", "strong electrolyte"),
        "hydrochloric acid": (3, "bright", "strong acid, fully ionised"),
        "sodium hydroxide": (3, "bright", "strong base, fully ionised"),
        "copper sulphate": (2, "moderate", "soluble salt, ions in solution"),
    }
    brightness, result, reason = table_data[solute]
    return {
        "kind": "qualitative",
        "table": [{"Solution": solute.title(), "Bulb": result, "Reason": reason}],
        "series": [],
        "notes": [
            "Conduction in solution requires mobile ions. Molecular substances such as "
            "sugar do not conduct, however concentrated the solution."
        ],
        "extras": [("Bulb brightness", f"{brightness}/3", "")],
        "observation": {
            "label": "Bulb",
            "colour": ["#374151", "#fbbf24", "#f59e0b", "#fde047"][brightness],
            "value": result,
        },
    }


def chromatography(solvent: str = "water-alcohol", seed: int | None = None) -> dict:
    rng = random.Random(seed)
    dyes = [
        ("Red dye", 0.75),
        ("Blue dye", 0.45),
        ("Green dye", 0.25),
    ]
    rows = []
    for name, rf in dyes:
        rf_meas = round(rf + rng.gauss(0, 0.01), 2)
        rows.append(
            {
                "Component": name,
                "Distance moved by dye (cm)": round(rf_meas * 8, 2),
                "Distance moved by solvent (cm)": 8.0,
                "Rf value": rf_meas,
            }
        )
    return {
        "kind": "quantitative",
        "measured": rows[1]["Rf value"],
        "accepted": 0.45,
        "table": rows,
        "series": [],
        "notes": [
            "Rf = distance moved by the component ÷ distance moved by the solvent front. "
            "Each dye has a characteristic Rf in a given solvent."
        ],
        "extras": [("Solvent", solvent, ""), ("Components separated", f"{len(dyes)}", "")],
        "observation": {"label": "Separation", "colour": "#a855f7", "value": "three spots resolved"},
    }


def heat_neutralisation(
    acid_conc: float = 1.0,
    base_conc: float = 1.0,
    volume_ml: float = 50.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    true_dh = -57.3  # kJ/mol
    n = acid_conc * volume_ml / 1000
    mass = 2 * volume_ml  # g, density 1
    c = 4.18
    dT_true = (-true_dh * 1000 * n) / (mass * c)

    rows, vals = [], []
    for trial in range(1, 4):
        dT = dT_true * (1 + rng.gauss(0, 0.02))
        dh = -(mass * c * dT) / (n * 1000)
        vals.append(dh)
        rows.append(
            {
                "Trial": trial,
                "Temperature rise ΔT (K)": round(dT, 2),
                "Heat evolved (J)": round(mass * c * dT, 0),
                "ΔH (kJ/mol)": round(dh, 2),
            }
        )
    measured = sum(vals) / len(vals)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": true_dh,
        "table": rows,
        "series": [],
        "notes": [
            "Heat evolved = m c ΔT. Dividing by the number of moles of water formed "
            "gives the molar enthalpy of neutralisation."
        ],
        "extras": [("Moles reacting", f"{n:.4f}", "mol"), ("Temperature rise", f"{dT_true:.2f}", "K")],
    }


def redox_kmno4(
    sample_mass_g: float = 1.0,
    fe_percent: float = 55.0,
    kmno4_conc: float = 0.01,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    n_fe = sample_mass_g * fe_percent / 100 / 55.85
    n_mn = n_fe / 5  # 5 Fe²⁺ : 1 MnO₄⁻
    v_eq_ml = n_mn / kmno4_conc * 1000

    rows, percents = [], []
    for trial in range(1, 4):
        v = v_eq_ml * (1 + rng.gauss(0, 0.01))
        n_fe_meas = 5 * kmno4_conc * v / 1000
        pct = n_fe_meas * 55.85 / sample_mass_g * 100
        percents.append(pct)
        rows.append(
            {
                "Trial": trial,
                "Volume of KMnO₄ (cm³)": round(v, 2),
                "Moles of Fe²⁺": round(n_fe_meas, 6),
                "Mass of Fe (g)": round(n_fe_meas * 55.85, 4),
                "% Fe": round(pct, 2),
            }
        )
    measured = sum(percents) / len(percents)
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": fe_percent,
        "table": rows,
        "series": [],
        "notes": [
            "MnO₄⁻ + 8H⁺ + 5Fe²⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O. One mole of permanganate "
            "oxidises five moles of iron(II)."
        ],
        "extras": [("Equivalence volume", f"{v_eq_ml:.2f}", "cm³")],
    }


def solubility_temperature(
    temperature_c: float = 40.0,
    seed: int | None = None,
) -> dict:
    rng = random.Random(seed)
    # KNO3-like curve
    true_s = 13.3 + 0.35 * temperature_c + 0.0045 * temperature_c**2
    rows, vals = [], []
    for trial in range(1, 4):
        s = true_s * (1 + rng.gauss(0, 0.01))
        vals.append(s)
        rows.append(
            {
                "Trial": trial,
                "Mass of evaporating dish (g)": 25.0,
                "Mass after evaporation (g)": round(25 + s / 10, 3),
                "Solubility (g per 100 g water)": round(s, 2),
            }
        )
    measured = sum(vals) / len(vals)
    xs = list(range(0, 101, 10))
    ys = [round(13.3 + 0.35 * t + 0.0045 * t**2, 1) for t in xs]
    return {
        "kind": "quantitative",
        "measured": measured,
        "accepted": true_s,
        "table": rows,
        "series": [
            {"name": "Solubility curve", "x": xs, "y": ys, "mode": "lines"},
            {"name": "Your point", "x": [temperature_c], "y": [round(measured, 1)], "mode": "markers"},
        ],
        "x_label": "Temperature (°C)",
        "y_label": "Solubility (g / 100 g water)",
        "notes": ["For most solids, solubility increases with temperature."],
        "extras": [("Temperature", f"{temperature_c:.0f}", "°C")],
    }


def salt_analysis(cation: str = "copper", seed: int | None = None) -> dict:
    data = {
        "ammonium": ("no precipitate; ammonia gas on warming", "#f1f5f9"),
        "magnesium": ("white precipitate, insoluble in excess NaOH", "#f8fafc"),
        "aluminium": ("white gelatinous precipitate, soluble in excess NaOH", "#f1f5f9"),
        "calcium": ("white precipitate, insoluble in excess NaOH", "#f8fafc"),
        "nickel": ("green precipitate", "#4ade80"),
        "cobalt": ("blue precipitate turning pink", "#f472b6"),
        "iron(II)": ("dirty green precipitate", "#4d7c0f"),
        "iron(III)": ("reddish-brown precipitate", "#b45309"),
        "copper": ("pale blue precipitate", "#60a5fa"),
        "zinc": ("white precipitate, soluble in excess NaOH", "#f8fafc"),
        "barium": ("white precipitate, insoluble in excess", "#f1f5f9"),
        "lead": ("white precipitate, soluble in excess NaOH", "#f8fafc"),
    }
    observation, colour = data[cation]
    return {
        "kind": "qualitative",
        "table": [{"Cation": cation, "Observation with NaOH": observation}],
        "series": [],
        "notes": [
            "Cations are identified by the colour of the hydroxide precipitate and by "
            "whether it dissolves in excess sodium hydroxide."
        ],
        "extras": [("Precipitate", observation, "")],
        "observation": {"label": "Observation", "colour": colour, "value": observation},
    }


def carbonyl_test(test: str = "tollens", sample: str = "aldehyde", seed: int | None = None) -> dict:
    data = {
        ("tollens", "aldehyde"): ("silver mirror on the tube", "#e5e7eb", "aldehyde present"),
        ("tollens", "ketone"): ("no change", "#f1f5f9", "no aldehyde"),
        ("fehling", "aldehyde"): ("brick-red precipitate", "#b91c1c", "aldehyde present"),
        ("fehling", "ketone"): ("stays blue", "#3b82f6", "no aldehyde"),
        ("benedict", "aldehyde"): ("brick-red precipitate", "#b91c1c", "aldehyde present"),
        ("benedict", "ketone"): ("stays blue", "#3b82f6", "no aldehyde"),
    }
    names = {"tollens": "Tollens' reagent", "fehling": "Fehling's solution", "benedict": "Benedict's solution"}
    observation, colour, conclusion = data[(test, sample)]
    return {
        "kind": "qualitative",
        "table": [{"Test": names[test], "Compound": sample, "Result": observation, "Conclusion": conclusion}],
        "series": [],
        "notes": [
            "Aldehydes are oxidised by Tollens' and Fehling's reagents; ketones are not. "
            "This is the standard way to distinguish an aldehyde from a ketone."
        ],
        "extras": [("Conclusion", conclusion, "")],
        "observation": {"label": observation, "colour": colour, "value": conclusion},
    }
