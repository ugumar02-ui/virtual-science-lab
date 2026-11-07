"""Virtual Science Lab API: runs the existing engines for the Flutter app."""

from __future__ import annotations

import os
import random
import secrets
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from content import GRADES, PRACTICALS, SUBJECTS, by_id
from core import get_engine

app = FastAPI(title="Virtual Science Lab API", version="1.0")

# Teacher mode needs this PIN. Empty = teacher mode disabled.
TEACHER_PIN = os.environ.get("LAB_TEACHER_PIN", "")


def clean(x: Any) -> Any:
    """Make engine output JSON-safe (tuples, numpy values, NaN/inf)."""
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if hasattr(x, "tolist"):
        return clean(x.tolist())
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        return None
    return x


def instructor_value(practical_id: str, ctrl: dict, seed: int):
    """Same hidden-value rule as the Streamlit renderer, so results match."""
    if ctrl["type"] not in {"slider", "number"}:
        return ctrl["default"]
    lo, hi, step = float(ctrl["min"]), float(ctrl["max"]), float(ctrl["step"])
    rng = random.Random(f"{practical_id}::{ctrl['key']}::{seed}")
    value = lo + rng.random() * (hi - lo)
    return round(round(value / step) * step, 6)


def coerce(ctrl: dict, value: Any):
    """Validate one visible control value against its schema."""
    if ctrl["type"] in {"slider", "number"}:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise HTTPException(422, f"{ctrl['key']} must be a number")
        return min(max(v, float(ctrl["min"])), float(ctrl["max"]))
    if ctrl["type"] == "select":
        if value not in ctrl["options"]:
            raise HTTPException(422, f"{ctrl['key']} must be one of {ctrl['options']}")
        return value
    raise HTTPException(500, f"Unknown control type {ctrl['type']!r}")


def is_teacher(pin: str | None) -> bool:
    if pin is None:
        return False
    if not TEACHER_PIN or not secrets.compare_digest(pin.encode(), TEACHER_PIN.encode()):
        raise HTTPException(403, "Invalid teacher PIN")
    return True


class RunRequest(BaseModel):
    controls: dict[str, Any] = Field(default_factory=dict)
    seed: int = 1
    teacher_pin: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "practicals": len(PRACTICALS)}


@app.get("/catalog")
def catalog():
    return clean({"subjects": SUBJECTS, "grades": GRADES, "practicals": PRACTICALS})


@app.post("/practicals/{practical_id}/run")
def run(practical_id: str, body: RunRequest):
    p = by_id(practical_id)
    if not p:
        raise HTTPException(404, f"Unknown practical {practical_id!r}")
    teacher = is_teacher(body.teacher_pin)

    params: dict[str, Any] = {}
    visible = []
    for ctrl in p.get("controls", []):
        if ctrl.get("teacher_only") and not teacher:
            params[ctrl["key"]] = instructor_value(p["id"], ctrl, body.seed)
        else:
            visible.append(ctrl)
    params.update(p.get("fixed", {}))
    for ctrl in visible:
        params[ctrl["key"]] = coerce(ctrl, body.controls.get(ctrl["key"], ctrl["default"]))

    try:
        result = get_engine(p["engine"])(**params, seed=body.seed)
    except Exception as exc:  # report engine bugs instead of crashing the server
        raise HTTPException(500, f"Engine error: {exc}")
    return {"practical_id": p["id"], "seed": body.seed, "teacher": teacher, "result": clean(result)}
