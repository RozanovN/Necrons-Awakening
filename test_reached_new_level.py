from unittest import TestCase
from game import reached_new_level as reached_new_level


class Test(TestCase):

    def test_reached_new_level_level_three(self):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}, "Level": [3, "abc"]}
        expected = False
        actual = reached_new_level(character)
        self.assertEqual(expected, actual)

    def test_reached_new_level_level_not_three_but_reached_new_level(self):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}, "Level": [2, "abc"],
                     "Current experience": 1000, "Experience for the next level": 500}
        expected = True
        actual = reached_new_level(character)
        self.assertEqual(expected, actual)

    def test_reached_new_level_level_not_three_but_not_reached_new_level(self):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}, 'Inventory': {}, "Level": [2, "abc"],
                     "Current experience": 1000, "Experience for the next level": 1500}
        expected = False
        actual = reached_new_level(character)
        self.assertEqual(expected, actual)
