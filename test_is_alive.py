from unittest import TestCase
from game import is_alive as is_alive


class TestAdd(TestCase):

    def test_is_alive_wounds_are_bigger_than_zero(self):
        character = {"X-coordinate": 0, "Y-coordinate": 1, "Current wounds": 5}
        expected = True
        actual = is_alive(character)
        self.assertEqual(expected, actual)

    def test_is_alive_wounds_are_zero(self):
        character = {"X-coordinate": 0, "Y-coordinate": 1, "Current wounds": 0}
        expected = False
        actual = is_alive(character)
        self.assertEqual(expected, actual)

    def test_is_alive_wounds_are_less_than_zero(self):
        character = {"X-coordinate": 0, "Y-coordinate": 1, "Current wounds": -1}
        expected = False
        actual = is_alive(character)
        self.assertEqual(expected, actual)