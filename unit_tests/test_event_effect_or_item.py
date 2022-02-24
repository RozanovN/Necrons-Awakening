from unittest import TestCase
from game import event_effect_or_item as event_effect_or_item
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_event_effect_or_item_check_if_event_with_effect_invoked(self, mock_stdout):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}}
        expected = "b"
        effect_or_item = {"Item": ["abc", "abc"]}
        event_effect_or_item(character, effect_or_item)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_event_effect_or_item_check_if_event_with_item_invoked(self, mock_stdout):
        character = {"Name": "Char", "Current wounds": 10, "Current experience": 0, "Characteristics": {"Agility": 40}}
        effect_or_item = {"Effect": ["abc", "abc"]}
        expected = "c"
        event_effect_or_item(character, effect_or_item)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)
