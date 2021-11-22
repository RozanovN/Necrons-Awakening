from unittest import TestCase
from game import bandage as bandage


class Test(TestCase):

    def test_bandage_has_item_and_current_wounds_are_not_equal_to_max_wounds(self):
        character = {"Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        expected = {"Current wounds": 14, "Max wounds": 20, "Inventory": {"Bandage": 4}}
        bandage(character)
        actual = character
        self.assertEqual(expected, actual)

    def test_bandage_has_item_and_current_wounds_are_close_to_max_wounds(self):
        character = {"Current wounds": 19, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        expected = {"Current wounds": 20, "Max wounds": 20, "Inventory": {"Bandage": 4}}
        bandage(character)
        actual = character
        self.assertEqual(expected, actual)

    def test_bandage_has_item_and_current_wounds_are_equal_to_max_wounds(self):
        character = {"Current wounds": 20, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        expected = {"Current wounds": 20, "Max wounds": 20, "Inventory": {"Bandage": 4}}
        bandage(character)
        actual = character
        self.assertEqual(expected, actual)

    def test_bandage_has_no_bandage(self):
        character = {"Current wounds": 15, "Max wounds": 20, "Inventory": {"Bandage": 0}}
        expected = {"Current wounds": 15, "Max wounds": 20, "Inventory": {"Bandage": 0}}
        bandage(character)
        actual = character
        self.assertEqual(expected, actual)
