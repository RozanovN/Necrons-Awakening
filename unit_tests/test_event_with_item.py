from unittest import TestCase
from game import event_with_item as event_with_item
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('random.choice', return_value=("Armor", "This cursed mechanical crown increases your wounds by 2."))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_event_with_item_check_item_description(self, mock_stdout, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Inventory": {}}
        expected = "This cursed mechanical crown increases your wounds by 2."
        items = []
        event_with_item(items, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('random.choice', return_value=("Armor", "This cursed mechanical crown increases your wounds by 2."))
    def test_event_with_item_check_item_armor(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Inventory": {}}
        expected = {"Name": "Char", "Max wounds": 12, "Current wounds": 12, "Inventory": {}}
        items = []
        event_with_item(items, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('random.choice', return_value=("Broken Armor", "This cursed mechanical crown increases your wounds by 1."))
    def test_event_with_item_check_item_broken_armor(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Inventory": {}}
        expected = {"Name": "Char", "Max wounds": 11, "Current wounds": 11, "Inventory": {}}
        items = []
        event_with_item(items, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('random.choice', return_value=("Torch", "You find a torch."))
    def test_event_with_item_check_item_in_inventory(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Inventory": {}}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Inventory": {"Torch": 1}}
        items = []
        event_with_item(items, character)
        actual = character
        self.assertEqual(expected, actual)
