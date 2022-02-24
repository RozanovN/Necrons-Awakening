from unittest import TestCase
from game import set_wounds as set_wounds
from unittest.mock import patch


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('builtins.input', return_value=5)
    def test_set_wounds_return_is_valid(self, _, __):
        expected = 22
        actual = set_wounds(character={"Name": "Test", "Adeptus": "Adeptus Astra Telepathica"})
        self.assertEqual(expected, actual)
