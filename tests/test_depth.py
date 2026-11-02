"""Checks the extended theory / viva material attached to every practical.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content import DEPTH, PRACTICALS  # noqa: E402


class TestDepthContent(unittest.TestCase):
    def test_every_practical_has_depth_content(self):
        missing = [p["id"] for p in PRACTICALS if not p.get("depth")]
        self.assertEqual(missing, [], f"practicals without depth content: {missing}")

    def test_no_orphan_depth_entries(self):
        ids = {p["id"] for p in PRACTICALS}
        extra = [pid for pid in DEPTH if pid not in ids]
        self.assertEqual(extra, [], f"depth entries with no practical: {extra}")

    def test_required_sections_are_present(self):
        required = {
            "objectives",
            "theory",
            "formula",
            "context",
            "precautions",
            "errors",
            "exam",
            "viva",
        }
        for p in PRACTICALS:
            depth = p["depth"]
            missing = required - depth.keys()
            self.assertEqual(missing, set(), f"{p['id']} missing {sorted(missing)}")

    def test_sections_are_substantial(self):
        for p in PRACTICALS:
            depth = p["depth"]
            self.assertGreaterEqual(len(depth["objectives"]), 3, p["id"])
            self.assertGreaterEqual(len(depth["theory"]), 2, p["id"])
            self.assertGreaterEqual(len(depth["precautions"]), 3, p["id"])
            self.assertGreaterEqual(len(depth["errors"]), 3, p["id"])
            self.assertGreaterEqual(len(depth["exam"]), 2, p["id"])
            self.assertGreaterEqual(len(depth["viva"]), 3, p["id"])

    def test_viva_entries_are_complete(self):
        for p in PRACTICALS:
            for i, qa in enumerate(p["depth"]["viva"]):
                self.assertIn("q", qa, f"{p['id']} viva {i}")
                self.assertIn("a", qa, f"{p['id']} viva {i}")
                self.assertTrue(qa["q"].strip(), f"{p['id']} viva {i} has an empty question")
                self.assertTrue(qa["a"].strip(), f"{p['id']} viva {i} has an empty answer")

    def test_depth_is_attached_from_the_same_object(self):
        for p in PRACTICALS:
            self.assertIs(p["depth"], DEPTH[p["id"]], p["id"])


if __name__ == "__main__":
    unittest.main()
