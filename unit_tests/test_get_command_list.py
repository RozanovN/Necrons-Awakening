from unittest import TestCase
from game import get_command_list as get_command_list


class Test(TestCase):
    def test_get_command_list(self):

        expected = ["q", "h", "b", "s", "i", "c"]
        actual = get_command_list()
        self.assertEqual(expected, actual)
