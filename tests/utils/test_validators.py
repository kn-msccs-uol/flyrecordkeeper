import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import unittest
from datetime import datetime
from utils import validators

class TestValidators(unittest.TestCase):

    # --- validate_required_field ---
    def test_required_field_missing(self):
        data = {}
        error = validators.validate_required_field(data, "name")
        self.assertEqual(error, "name is required")

    def test_required_field_empty_string(self):
        data = {"name": "   "}
        error = validators.validate_required_field(data, "name")
        self.assertEqual(error, "name cannot be empty")

    def test_required_field_present(self):
        data = {"name": "Kevin"}
        error = validators.validate_required_field(data, "name")
        self.assertIsNone(error)

    # --- validate_string ---
    def test_validate_string_valid(self):
        error = validators.validate_string("Kevin", "Name")
        self.assertIsNone(error)

    def test_validate_string_not_string(self):
        error = validators.validate_string(123, "Name")
        self.assertEqual(error, "Name must be a string")

    def test_validate_string_too_short(self):
        error = validators.validate_string("A", "Name", min_length=2)
        self.assertEqual(error, "Name must be at least 2 characters")

    def test_validate_string_too_long(self):
        error = validators.validate_string("A" * 101, "Name", max_length=100)
        self.assertEqual(error, "Name must be at most 100 characters")

    # --- validate_integer ---
    def test_validate_integer_valid(self):
        error = validators.validate_integer(5, "Age", min_value=1, max_value=10)
        self.assertIsNone(error)

    def test_validate_integer_not_int(self):
        error = validators.validate_integer("five", "Age")
        self.assertEqual(error, "Age must be an integer")

    def test_validate_integer_too_small(self):
        error = validators.validate_integer(0, "Age", min_value=1)
        self.assertEqual(error, "Age must be at least 1")

    def test_validate_integer_too_large(self):
        error = validators.validate_integer(101, "Age", max_value=100)
        self.assertEqual(error, "Age must be at most 100")

    # --- validate_phone_number ---
    def test_validate_phone_number_valid(self):
        valid_numbers = ["+44 1234 567890", "(123) 456-7890", "123-456-7890"]
        for number in valid_numbers:
            self.assertIsNone(validators.validate_phone_number(number))

    def test_validate_phone_number_invalid_chars(self):
        error = validators.validate_phone_number("abc123")
        self.assertEqual(error, "Phone number contains invalid characters")

    def test_validate_phone_number_missing_digits(self):
        error = validators.validate_phone_number("+++")
        self.assertEqual(error, "Phone number must contain some digits")

    # --- validate_date ---
    def test_validate_date_valid(self):
        error = validators.validate_date(datetime.now())
        self.assertIsNone(error)

    def test_validate_date_invalid(self):
        error = validators.validate_date("2025-01-01")
        self.assertEqual(error, "Date must be a datetime object")

if __name__ == "__main__":
    unittest.main()

