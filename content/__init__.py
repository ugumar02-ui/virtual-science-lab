"""Practical catalogue — AKU-EB SSC and HSSC Physics, Chemistry and Biology."""

from .biology import BIOLOGY
from .chemistry import CHEMISTRY
from .physics import PHYSICS
from .syllabus_map import OFFICIAL_COUNTS, SYLLABUS

PRACTICALS: list[dict] = PHYSICS + CHEMISTRY + BIOLOGY

# Attach the official AKU-EB reference to every practical so the UI can show
# exactly which syllabus line each simulation covers.
for _p in PRACTICALS:
    _p["syllabus"] = SYLLABUS.get(_p["id"], {})

SUBJECTS = {
    "physics": {"label": "Physics", "icon": "⚛️", "colour": "#2563eb"},
    "chemistry": {"label": "Chemistry", "icon": "⚗️", "colour": "#059669"},
    "biology": {"label": "Biology", "icon": "🧬", "colour": "#d97706"},
}

GRADES = ["IX", "X", "XI", "XII"]


def level_of(grade: str) -> str:
    return "SSC" if grade in ("IX", "X") else "HSSC"


def by_id(practical_id: str) -> dict | None:
    for p in PRACTICALS:
        if p["id"] == practical_id:
            return p
    return None
