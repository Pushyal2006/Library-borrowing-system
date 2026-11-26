
import unittest
import tempfile
import os

from datetime import date

from src.library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_directory = os.getcwd()
        os.chdir(self.temp_dir.name)

        self.library = Library()

        self.library.add_member(
            "M001", "Rahul", "rahul@example.com"
        )

        self.library.add_resource(
            "B001", "Python Programming", "book"
        )

        self.library.add_resource(
            "D001", "Python Digital Guide", "digital"
        )

    def tearDown(self):
        os.chdir(self.original_directory)
        self.temp_dir.cleanup()

    def test_add_member(self):
        member = self.library.add_member(
            "M002", "Amit", "amit@example.com"
        )
        self.assertEqual(member.name, "Amit")

    def test_duplicate_member(self):
        with self.assertRaises(ValueError):
            self.library.add_member(
                "M001", "Duplicate", "duplicate@example.com"
            )

    def test_empty_member_fields(self):
        with self.assertRaises(ValueError):
            self.library.add_member("", "", "")

    def test_add_book(self):
        book = self.library.add_resource(
            "B002", "Data Structures", "book"
        )
        self.assertEqual(book.loan_days(), 14)
        self.assertEqual(book.fine_per_day(), 2.0)

    def test_digital_rules(self):
        digital = self.library.list_resources()[1]
        self.assertEqual(digital.loan_days(), 7)
        self.assertEqual(digital.fine_per_day(), 1.0)

    def test_duplicate_resource(self):
        with self.assertRaises(ValueError):
            self.library.add_resource(
                "B001", "Another Book", "book"
            )

    def test_issue_resource(self):
        today = date(2026, 1, 1)

        loan = self.library.issue_resource(
            "M001", "B001", today
        )

        self.assertEqual(loan.loan_id, "L001")
        self.assertEqual(loan.due_date, date(2026, 1, 15))
        self.assertFalse(
            self.library._find_resource("B001")["available"]
        )

    def test_issue_already_issued(self):
        today = date(2026, 1, 1)

        self.library.issue_resource(
            "M001", "B001", today
        )

        with self.assertRaises(ValueError):
            self.library.issue_resource(
                "M001", "B001", today
            )

    def test_unknown_member(self):
        with self.assertRaises(ValueError):
            self.library.issue_resource(
                "UNKNOWN", "B001"
            )

    def test_unknown_resource(self):
        with self.assertRaises(ValueError):
            self.library.issue_resource(
                "M001", "UNKNOWN"
            )

    def test_return_on_due_date(self):
        today = date(2026, 1, 1)

        loan = self.library.issue_resource(
            "M001", "B001", today
        )

        result = self.library.return_resource(
            loan.loan_id, date(2026, 1, 15)
        )

        self.assertEqual(result["overdue_days"], 0)
        self.assertEqual(result["fine"], 0.0)

    def test_return_late(self):
        today = date(2026, 1, 1)

        loan = self.library.issue_resource(
            "M001", "B001", today
        )

        result = self.library.return_resource(
            loan.loan_id, date(2026, 1, 17)
        )

        self.assertEqual(result["overdue_days"], 2)
        self.assertEqual(result["fine"], 4.0)

    def test_return_twice(self):
        today = date(2026, 1, 1)

        loan = self.library.issue_resource(
            "M001", "B001", today
        )

        self.library.return_resource(
            loan.loan_id, today
        )

        with self.assertRaises(ValueError):
            self.library.return_resource(
                loan.loan_id, today
            )

    def test_reconciliation(self):
        today = date(2026, 1, 1)

        self.library.issue_resource(
            "M001", "B001", today
        )

        self.library.issue_resource(
            "M001", "D001", today
        )

        report = self.library.reconciliation_report(
            date(2026, 1, 17)
        )

        self.assertEqual(report["issued"], 2)
        self.assertEqual(report["returned"], 0)
        self.assertEqual(report["overdue"], 2)
        self.assertEqual(report["outstanding_fines"], 13.0)


if __name__ == "__main__":
    unittest.main()
