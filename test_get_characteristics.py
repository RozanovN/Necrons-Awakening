from unittest import TestCase
from game import get_characteristics as get_characteristics
from unittest.mock import patch


class Test(TestCase):

    @patch('builtins.input', return_value="1")
    @patch('game.roll', return_value=5)
    def test_get_characteristics_return_is_valid(self, _, __):
        character = {"Name": "Char", "Adeptus": "Adeptus Astra Telepathica"}
        expected = {"Intellect": 35, "Strength": 35, "Toughness": 35, "Agility": 35}
        actual = get_characteristics(character)
        self.assertEqual(expected, actual)
