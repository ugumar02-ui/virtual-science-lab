"""Checks that every practical traces back to the official AKU-EB syllabus.

Run:  .venv/bin/python -m unittest discover -s tests -v
"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from content import PRACTICALS  # noqa: E402
from content.syllabus_map import OFFICIAL_COUNTS, SYLLABUS  # noqa: E402


class TestSyllabusMap(unittest.TestCase):
    def test_every_practical_has_a_syllabus_entry(self):
        missing = [p["id"] for p in PRACTICALS if p["id"] not in SYLLABUS]
        self.assertEqual(missing, [], f"practicals without a syllabus line: {missing}")

    def test_no_orphan_syllabus_entries(self):
        ids = {p["id"] for p in PRACTICALS}
        extra = [pid for pid in SYLLABUS if pid not in ids]
        self.assertEqual(extra, [], f"syllabus entries with no practical: {extra}")

    def test_every_entry_has_reference_and_activity(self):
        for pid, entry in SYLLABUS.items():
            self.assertTrue(entry.get("ref"), f"{pid} has no ref")
            self.assertTrue(entry.get("activity"), f"{pid} has no activity")

    def test_reference_subject_and_grade_match_the_practical(self):
        names = {"physics": "Physics", "chemistry": "Chemistry", "biology": "Biology"}
        for p in PRACTICALS:
            ref = SYLLABUS[p["id"]]["ref"]
            match = re.match(r"^(Physics|Chemistry|Biology)\s+(XII|XI|X|IX)\b", ref)
            self.assertIsNotNone(match, f"{p['id']} has an unreadable ref: {ref!r}")
            subject, grade = match.groups()
            self.assertEqual(subject, names[p["subject"]], p["id"])
            self.assertEqual(grade, p["grade"], p["id"])

    def test_official_counts_cover_every_grade(self):
        for subject, grades in OFFICIAL_COUNTS.items():
            self.assertEqual(set(grades), {"IX", "X", "XI", "XII"}, subject)
            for grade, count in grades.items():
                self.assertGreater(count, 0, f"{subject} {grade}")

    def test_built_practicals_never_exceed_official_count(self):
        for p in PRACTICALS:
            official = OFFICIAL_COUNTS[p["subject"]][p["grade"]]
            built = sum(
                1
                for q in PRACTICALS
                if q["subject"] == p["subject"] and q["grade"] == p["grade"]
            )
            self.assertLessEqual(built, official, f"{p['subject']} {p['grade']}")


if __name__ == "__main__":
    unittest.main()
