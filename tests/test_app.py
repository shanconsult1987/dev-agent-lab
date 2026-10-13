
import unittest

from app import make_plan


class TestPlanner(unittest.TestCase):
    def test_creates_plan(self):
        plan = make_plan("Add task priority")

        self.assertEqual(plan["request"], "Add task priority")
        self.assertEqual(plan["status"], "planned")
        self.assertTrue(plan["steps"])
        self.assertTrue(plan["acceptance_criteria"])

    def test_rejects_empty_request(self):
        with self.assertRaises(ValueError):
            make_plan("")

    def test_rejects_whitespace_request(self):
        with self.assertRaises(ValueError):
            make_plan("   ")


if __name__ == "__main__":
    unittest.main()
