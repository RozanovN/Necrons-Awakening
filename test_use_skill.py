from unittest import TestCase
from game import use_skill as use_skill
from unittest.mock import patch


class Test(TestCase):

    @patch('game.spontaneous_combustion', return_value=5)
    def test_use_skill_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 5
        actual = use_skill(character, "Spontaneous Combustion", enemy)
        self.assertEqual(expected, actual)
