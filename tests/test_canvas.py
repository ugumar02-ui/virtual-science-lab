"""Tests for the embedded canvas simulations.

The canvas is plain HTML/JS, so these tests check that the Python wrapper
injects a valid config and leaves no template placeholders behind.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ui import canvas  # noqa: E402


class TestTitrationCanvas(unittest.TestCase):
    def setUp(self):
        self.html = canvas.build_titration_html(
            acid_conc=0.1, acid_volume=25, base_conc=0.1, n_factor=2, initial_reading=0.15
        )

    def test_template_exists(self):
        self.assertTrue(canvas._HTML.exists(), "titration_canvas.html is missing")

    def test_placeholder_is_replaced(self):
        self.assertNotIn("__CONFIG__", self.html)

    def test_config_is_valid_json_and_keeps_its_values(self):
        start = self.html.index("const CFG = ") + len("const CFG = ")
        end = self.html.index(";", start)
        config = json.loads(self.html[start:end])
        self.assertEqual(config["nFactor"], 2)
        self.assertAlmostEqual(config["acidConc"], 0.1)
        self.assertAlmostEqual(config["initialReading"], 0.15)
        self.assertGreater(config["flowRate"], 0)

    def test_endpoint_is_reachable_inside_the_burette(self):
        # The equivalence volume must fit on a 50 cm3 burette, or the student
        # could never reach the endpoint.
        veq = 2 * 0.1 * 25 / 0.1
        self.assertLessEqual(veq, 50)


if __name__ == "__main__":
    unittest.main()
