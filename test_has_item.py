from unittest import TestCase
from game import has_item as has_item


class Test(TestCase):

    def test_has_item_no_item(self):
        character = {"Name": "Char", "Inventory": {"Bandage": 5}}
        expected = False
        actual = has_item("Torch", character)
        self.assertEqual(expected, actual)

    def test_has_item_item_is_present(self):
        character = {"Name": "Char", "Inventory": {"Shovel": 5}}
        expected = True
        actual = has_item("Shovel", character)
        self.assertEqual(expected, actual)
