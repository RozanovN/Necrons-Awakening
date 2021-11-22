from unittest import TestCase
from game import is_goal_attained as is_goal_attained


class Test(TestCase):

    def test_is_goal_attained_goal_is_not_attained(self):
        expected = False
        character = {}
        actual = is_goal_attained(character)
        self.assertEqual(expected, actual)

    def test_is_goal_attained_goal_is_attained(self):
        expected = True
        character = {"Artifact": "anything"}
        actual = is_goal_attained(character)
        self.assertEqual(expected, actual)
