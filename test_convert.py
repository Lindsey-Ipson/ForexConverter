from convert import validate_curr_code
from unittest import TestCase


class ValidateCurrCodeTestCase(TestCase):
    """Ensure correct currency codes return valid while nonexistent ones return invalid"""

    def test_validate_curr_code(self):
        self.assertEqual(validate_curr_code('USD'), 'valid')
        self.assertEqual(validate_curr_code('GBP'), 'valid')
        self.assertEqual(validate_curr_code('ZZZ'), 'invalid')
        self.assertEqual(validate_curr_code('YYY'), 'invalid')
        self.assertEqual(validate_curr_code(''), 'invalid')
        self.assertEqual(validate_curr_code('123'), 'invalid')

    