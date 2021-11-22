from unittest import TestCase
from game import event_with_input as event_with_input
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.event_effect_or_item', return_value=1)
    @patch('game.print_numbered_list_of_possibilities', return_value=1)
    @patch('game.process_input', return_value=2)
    @patch('game.has_item', return_value=False)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_event_with_check_of_item_description(self, mock_stdout, _, __, ___, ____):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}}
        expected = "abc"
        event = {"Input": {"Description": "abc", "No": "abc"}}
        event_with_input(character, event)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.event_effect_or_item', return_value=1)
    @patch('game.print_numbered_list_of_possibilities', return_value=1)
    @patch('game.process_input', return_value=1)
    @patch('game.has_item', return_value=False)
    def test_event_with_check_of_item_after_effect(self, _, __, ___, ____):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}}
        expected = {"Input": {"Description": "abc", "Yes": "abc"}, "After-effect": True}
        event = {"Input": {"Description": "abc", "Yes": "abc"}, "After-effect": False}
        event_with_input(character, event)
        actual = event
        self.assertEqual(expected, actual)
