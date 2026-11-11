import unittest

from task2.session import run_session


class SessionLockoutTests(unittest.TestCase):
    def test_locks_after_three_consecutive_failures(self):
        self.assertEqual(run_session("WWW")[0], "LOCKED")

    def test_correct_attempt_resets_failure_streak(self):
        self.assertEqual(run_session("WWCWW")[0], "TWO_WRONG")

    def test_locked_state_is_absorbing(self):
        self.assertEqual(run_session("WWWCC")[0], "LOCKED")

    def test_rejects_unknown_event(self):
        with self.assertRaises(ValueError):
            run_session("WX")


if __name__ == "__main__":
    unittest.main()

