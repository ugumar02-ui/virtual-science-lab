"""Embedded interactive canvas simulations (Tier 2).

These are self-contained HTML/JS widgets rendered in an iframe. The physics is
done in JavaScript so the animation runs at 60 fps in the browser; Python only
supplies the starting conditions.
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit.components.v1 as components

_HTML = Path(__file__).with_name("titration_canvas.html")


def build_titration_html(
    acid_conc: float,
    acid_volume: float,
    base_conc: float,
    n_factor: int = 1,
    initial_reading: float = 0.0,
) -> str:
    """Return the canvas HTML with the starting conditions injected."""
    config = {
        "acidConc": acid_conc,
        "acidVolume": acid_volume,
        "baseConc": base_conc,
        "nFactor": n_factor,
        "initialReading": initial_reading,
        "flowRate": 0.6,  # cm3 per second with the tap fully open
    }
    return _HTML.read_text(encoding="utf-8").replace("__CONFIG__", json.dumps(config))


def titration_canvas(
    acid_conc: float,
    acid_volume: float,
    base_conc: float,
    n_factor: int = 1,
    initial_reading: float = 0.0,
    height: int = 560,
) -> None:
    """A real burette: open the tap, watch the drops, close it at the pink flash."""
    components.html(
        build_titration_html(acid_conc, acid_volume, base_conc, n_factor, initial_reading),
        height=height,
        scrolling=False,
    )
