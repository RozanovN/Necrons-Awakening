from unittest import TestCase
from game import set_name as set_name
from unittest.mock import patch


class Test(TestCase):

    @patch('builtins.input', return_value="abc")
    def test_set_name_return_is_valid(self, _):
        expected = "Abc"
        actual = set_name()
        self.assertEqual(expected, actual)
