"""Guardrails for the public SQL demo fixture (stdlib-only tests)."""
from pathlib import Path
import re
import unittest

SQL = (Path(__file__).resolve().parents[1] / "librarydb.sql").read_text(encoding="utf-8")
START = "-- BEGIN PUBLIC SYNTHETIC DEMO DATA"
END = "-- END PUBLIC SYNTHETIC DEMO DATA"
TABLES = {"books", "borrowedbooks", "fines", "librarians", "members", "questions", "transactions"}
COUNTS = {"books": 3, "members": 2, "librarians": 1, "borrowedbooks": 2, "fines": 1, "questions": 1, "transactions": 2}


def inserts(text: str):
    return re.findall(r"(?ims)^INSERT INTO `(\w+)`\s*\([^;]*?;", text)


class PublicFixtureTests(unittest.TestCase):
    def test_schema_preserves_seven_tables(self):
        self.assertEqual(set(re.findall(r"(?im)^CREATE TABLE `(\w+)`", SQL)), TABLES)
        self.assertEqual(len(re.findall(r"(?im)^\s+ADD CONSTRAINT `", SQL)), 8)

    def test_no_imported_insert_statements_outside_fixture(self):
        self.assertEqual(SQL.count(START), 1)
        self.assertEqual(SQL.count(END), 1)
        before, after_start = SQL.split(START)
        fixture, after = after_start.split(END)
        self.assertNotRegex(before + after, r"(?im)^INSERT INTO ")
        self.assertEqual(set(inserts(fixture)), TABLES)
        self.assertEqual(len(inserts(fixture)), 7)

    def test_only_reserved_email_addresses(self):
        fixture = SQL.split(START, 1)[1].split(END, 1)[0]
        emails = re.findall(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", fixture)
        self.assertEqual(len(emails), 3)
        self.assertTrue(all(email.endswith("@example.invalid") for email in emails))

    def test_demo_accounts_are_not_usable(self):
        fixture = SQL.split(START, 1)[1].split(END, 1)[0]
        self.assertEqual(fixture.count("'DISABLED_ACCOUNT_CREATE_LOCALLY'"), 3)
        self.assertNotRegex(fixture, r"\b[a-fA-F0-9]{64}\b")
        self.assertNotIn("@montclair.edu", fixture.lower())
        self.assertIn("'Demo Member One'", fixture)
        self.assertIn("'Demo Member Two'", fixture)
        self.assertIn("'Demo Librarian'", fixture)
        self.assertEqual(fixture.count("NULL, NULL, 'DISABLED_ACCOUNT_CREATE_LOCALLY'"), 2)

    def test_expected_synthetic_relationships(self):
        fixture = SQL.split(START, 1)[1].split(END, 1)[0]
        for table, expected in COUNTS.items():
            self.assertRegex(fixture, rf"(?i)INSERT INTO `{table}`")
            self.assertGreater(expected, 0)
        self.assertIn("DATE_SUB(CURDATE(), INTERVAL 20 DAY)", fixture)
        self.assertIn("DATE_ADD(CURDATE(), INTERVAL 12 DAY)", fixture)


if __name__ == "__main__":
    unittest.main()
