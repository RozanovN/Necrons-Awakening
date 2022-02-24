from unittest import TestCase
from game import has_argument as has_argument


class Test(TestCase):

    def test_has_argument_command_has_no_argument(self):
        expected = False
        actual = has_argument("h")
        self.assertEqual(expected, actual)

    def test_has_argument_command_has_argument(self):
        expected = True
        actual = has_argument("b")
        self.assertEqual(expected, actual)
