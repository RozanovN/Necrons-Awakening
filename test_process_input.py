from unittest import TestCase
from game import process_input as process_input
from unittest.mock import patch


class Test(TestCase):

    @patch('game.validate_option', return_value=True)
    @patch('builtins.input', return_value="1")
    def test_event_with_check_of_item_description(self, _, __):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}}
        expected = "1"
        list_of_options = ["test", "test"]
        actual = process_input(character, list_of_options)
        self.assertEqual(expected, actual)
