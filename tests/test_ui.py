"""Checks the presentation layer stays in sync with the catalogue."""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content import PRACTICALS  # noqa: E402
from core import registry  # noqa: E402
from ui import bench  # noqa: E402
from ui.renderer import _report, _visible_extras  # noqa: E402


class TestPresentation(unittest.TestCase):
    def test_every_practical_has_an_apparatus_scene(self):
        missing = [p["id"] for p in PRACTICALS if p["id"] not in bench._SCENES]
        self.assertEqual(missing, [], f"practicals without an apparatus scene: {missing}")

    def test_every_scene_renders_svg(self):
        for p in PRACTICALS:
            params = {c["key"]: c["default"] for c in p.get("controls", [])}
            params.update(p.get("fixed", {}))
            result = registry.get_engine(p["engine"])(**params, seed=1)
            html = bench._SCENES[p["id"]](params, result)
            self.assertIn("<svg", html, p["id"])
            self.assertIn("</svg>", html, p["id"])
            self.assertNotIn("    <rect", html, f"{p['id']} has indented markup")

    def test_scene_geometry_responds_to_controls(self):
        p = {item["id"]: item for item in PRACTICALS}["phy-vernier-ix"]
        base = {c["key"]: c["default"] for c in p["controls"]}
        engine = registry.get_engine(p["engine"])
        narrow = bench._caliper({**base, "true_diameter_mm": 10}, engine(**base, seed=1))
        wide = bench._caliper({**base, "true_diameter_mm": 40}, engine(**base, seed=1))

        def jaw_x(html: str) -> float:
            match = re.search(r'<rect x="([\d.]+)" y="104" width="26"', html)
            self.assertIsNotNone(match)
            return float(match.group(1))

        # The sliding jaw sits further right for the wider object.
        self.assertLess(jaw_x(narrow), jaw_x(wide))

    def test_scene_responds_to_zero_error(self):
        p = {item["id"]: item for item in PRACTICALS}["phy-vernier-ix"]
        base = {c["key"]: c["default"] for c in p["controls"]}
        engine = registry.get_engine(p["engine"])
        zero = bench._caliper({**base, "zero_error_mm": 0.0}, engine(**base, seed=1))
        shifted = bench._caliper({**base, "zero_error_mm": 0.1}, engine(**base, seed=1))
        self.assertNotEqual(zero, shifted)
        self.assertIn("zero +0.10 mm", shifted)

    def test_scene_colours_respond_to_selection(self):
        p = {item["id"]: item for item in PRACTICALS}["chem-ph-x"]
        base = {c["key"]: c["default"] for c in p["controls"]}
        engine = registry.get_engine(p["engine"])
        acid = bench._ph({**base, "substance": "lemon juice"}, engine(**base, seed=1))
        alkali = bench._ph({**base, "substance": "caustic soda"}, engine(**base, seed=1))
        self.assertNotEqual(acid, alkali)

    def test_report_includes_extended_material(self):
        p = PRACTICALS[0]
        params = {c["key"]: c["default"] for c in p.get("controls", [])}
        params.update(p.get("fixed", {}))
        result = registry.get_engine(p["engine"])(**params, seed=1)
        report = _report(p, result, 0.1)
        for heading in (
            "Learning objectives",
            "Theory",
            "Sources of error",
            "Exam tips",
            "Viva questions",
            "Precautions",
        ):
            self.assertIn(heading, report, f"{p['id']} report missing {heading}")

    def test_duplicate_headline_extras_are_hidden(self):
        result = {
            "extras": [("Isotonic concentration", "0.292", "mol/dm³"), ("Immersion time", "30", "min")]
        }
        quantity = {"label": "Isotonic concentration", "unit": "mol/dm³"}
        labels = [e[0] for e in _visible_extras(result, quantity)]
        self.assertEqual(labels, ["Immersion time"])

    def test_single_redundant_extra_is_hidden(self):
        result = {"extras": [("Rate", "48.3", "bubbles/min")]}
        quantity = {"label": "Rate of oxygen release", "unit": "bubbles/min"}
        self.assertEqual(_visible_extras(result, quantity), [])


if __name__ == "__main__":
    unittest.main()
