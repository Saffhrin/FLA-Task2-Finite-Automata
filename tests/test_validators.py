import unittest
from itertools import product

from fa_validators.session import run_session
from fa_validators.validators import EMAIL_CLASSES, EMAIL_DFA, EMAIL_MIN_DFA, EMAIL_NFA, validate_email, validate_email_dfa, validate_email_min_dfa, validate_password, validate_pin


class ValidatorTests(unittest.TestCase):
    def test_password_accepts_policy_examples(self):
        for value in ("Abcdef1!", "Stronger9#word", "A1aaaaa!", "Qwerty7$", "Passcode2@"):
            with self.subTest(value=value):
                self.assertTrue(validate_password(value))

    def test_password_rejects_policy_violations(self):
        for value in ("Ab1!xyz", "abcdefgh1!", "ABCDEFGH1!", "Abcdefgh!", "Abcdefg1"):
            with self.subTest(value=value):
                self.assertFalse(validate_password(value))

    def test_email_subset_examples(self):
        for value in ("user@gmail.com", "student123@yahoo.in", "a@b.co", "first.last@sub.example.org", "x@y.ab"):
            with self.subTest(value=value):
                self.assertTrue(validate_email(value))
        for value in ("@gmail.com", "user@gmail", "user@.com", "user@domain.c", "user@@domain.com", ".user@domain.com", "user.@domain.com", "user..name@domain.com", "user@domain..com"):
            with self.subTest(value=value):
                self.assertFalse(validate_email(value))

    def test_email_nfa_and_subset_dfa_agree(self):
        examples = (
            "user@gmail.com", "student123@yahoo.in", "a@b.co",
            "first.last@sub.example.org", "x@y.ab", "@gmail.com",
            "user@domain.c", "user..name@domain.com", "user@domain..com",
        )
        self.assertGreater(len(EMAIL_DFA.reachable_states(EMAIL_CLASSES)), 2)
        self.assertLessEqual(len(EMAIL_MIN_DFA.reachable_states(EMAIL_CLASSES)), len(EMAIL_DFA.reachable_states(EMAIL_CLASSES)))
        for value in examples:
            with self.subTest(value=value):
                self.assertEqual(validate_email(value), validate_email_dfa(value))
                self.assertEqual(validate_email(value), validate_email_min_dfa(value))

    def test_email_nfa_has_a_real_branch_at_domain_dot(self):
        targets = EMAIL_NFA.transition("domain_word", ".")
        self.assertEqual(targets, frozenset({"domain_after_dot", "tld_first"}))

    def test_email_models_agree_on_all_short_class_strings(self):
        alphabet = EMAIL_CLASSES
        for size in range(5):
            for symbols in product(alphabet, repeat=size):
                value = "".join(symbols)
                with self.subTest(value=value):
                    expected = validate_email(value)
                    self.assertEqual(expected, validate_email_dfa(value))
                    self.assertEqual(expected, validate_email_min_dfa(value))

    def test_pin_accepts_and_rejects(self):
        for value in ("1234", "0000", "9087", "5678", "2468"):
            self.assertTrue(validate_pin(value))
        for value in ("123", "12345", "12A4", "１２３４", ""):
            self.assertFalse(validate_pin(value))


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
