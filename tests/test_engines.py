"""Smoke tests for the simulation engines.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content import PRACTICALS, by_id  # noqa: E402
from core import get_engine  # noqa: E402


class TestCatalogue(unittest.TestCase):
    def test_ids_are_unique(self):
        ids = [p["id"] for p in PRACTICALS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_practical_has_required_fields(self):
        for p in PRACTICALS:
            for field in ("id", "subject", "grade", "title", "engine", "theory"):
                self.assertIn(field, p, f"{p.get('id')} is missing {field}")
            self.assertIn(p["grade"], ("IX", "X", "XI", "XII"))

    def test_every_practical_covers_both_levels(self):
        levels = {p["grade"] in ("IX", "X") for p in PRACTICALS}
        self.assertEqual(levels, {True, False})


class TestEngines(unittest.TestCase):
    def test_all_engines_run_with_defaults(self):
        for p in PRACTICALS:
            defaults = {c["key"]: c["default"] for c in p.get("controls", [])}
            engine = get_engine(p["engine"])
            result = engine(**defaults, seed=7)
            self.assertIn(result.get("kind"), ("quantitative", "qualitative"), p["id"])
            if result["kind"] == "quantitative":
                self.assertIsInstance(result["measured"], (int, float), p["id"])
                self.assertIsInstance(result["accepted"], (int, float), p["id"])
                self.assertFalse(
                    math.isnan(result["measured"]), f"{p['id']} produced NaN"
                )

    def test_pendulum_recovers_g(self):
        result = get_engine("physics.engines.pendulum")(length_cm=100, seed=1)
        self.assertAlmostEqual(result["measured"], 9.81, delta=0.6)

    def test_titration_recovers_concentration(self):
        result = get_engine("chemistry.engines.titration")(
            acid_conc=0.1, acid_volume=25, base_conc=0.1, seed=1
        )
        self.assertAlmostEqual(result["measured"], 0.1, delta=0.005)

    def test_diprotic_titration_uses_two_to_one_ratio(self):
        result = get_engine("chemistry.engines.titration")(
            acid_conc=0.05, acid_volume=25, base_conc=0.1, n_factor=2, seed=1
        )
        self.assertAlmostEqual(result["measured"], 0.05, delta=0.004)

    def test_ohm_law_recovers_resistance(self):
        result = get_engine("physics.engines.ohm_law")(resistance_ohm=10, seed=1)
        self.assertAlmostEqual(result["measured"], 10, delta=0.5)

    def test_series_and_parallel(self):
        eng = get_engine("physics.engines.series_parallel")
        self.assertAlmostEqual(eng(r1=10, r2=20, mode="series", seed=1)["measured"], 30, delta=0.5)
        self.assertAlmostEqual(
            eng(r1=10, r2=20, mode="parallel", seed=1)["measured"], 6.67, delta=0.2
        )

    def test_rc_time_constant(self):
        result = get_engine("physics.engines.rc_circuit")(
            resistance_kohm=10, capacitance_uf=100, seed=1
        )
        self.assertAlmostEqual(result["measured"], 1.0, delta=0.05)

    def test_specific_heat_of_copper(self):
        result = get_engine("physics.engines.specific_heat")(metal="copper", seed=1)
        self.assertAlmostEqual(result["measured"], 380, delta=25)

    def test_enzyme_has_optimum_near_37(self):
        eng = get_engine("biology.engines.enzyme")
        opt = eng(temperature_c=40, ph=7, enzyme_name="amylase", seed=1)["extras"][2][1]
        cold = eng(temperature_c=5, ph=7, enzyme_name="amylase", seed=1)["extras"][2][1]
        self.assertGreater(float(opt.rstrip("%")), float(cold.rstrip("%")))

    def test_food_test_is_qualitative(self):
        result = get_engine("biology.engines.food_test")(test="iodine", sample="potato")
        self.assertEqual(result["kind"], "qualitative")
        self.assertIn("observation", result)

    def test_every_practical_id_resolves(self):
        for p in PRACTICALS:
            self.assertIsNotNone(by_id(p["id"]))


if __name__ == "__main__":
    unittest.main()
