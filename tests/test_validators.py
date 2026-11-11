import unittest

from task2.validators import validate_email, validate_password, validate_pin


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
        for value in ("@gmail.com", "user@gmail", "user@.com", "user@domain.c", "user@@domain.com"):
            with self.subTest(value=value):
                self.assertFalse(validate_email(value))

    def test_pin_accepts_and_rejects(self):
        for value in ("1234", "0000", "9087", "5678", "2468"):
            self.assertTrue(validate_pin(value))
        for value in ("123", "12345", "12A4", "１２３４", ""):
            self.assertFalse(validate_pin(value))


if __name__ == "__main__":
    unittest.main()
