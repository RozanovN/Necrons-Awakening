from unittest import TestCase
from game import combat as combat
from unittest.mock import patch


class Test(TestCase):

    @patch('builtins.input', return_value="1")
    def test_combat_experience_received(self, _):
        character = {
            "Name": "Horus",
            "Adeptus": "Adeptus Mechanicus",
            "Max wounds": 25,
            "Current wounds": 25,
            "Characteristics": {"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39},
            "Level": (1, "Acolyte"),
            "Skills": {
                "Flee Away": "You retreat to the previous room.",
                "Laser Shot": "Your servo-skull shots a laser beam from its eyes "
                              "dealing (3 + Intellect Bonus) damage."
            },
            "Current experience": 0,
            "Experience for the next level": 1000,
            "Will to fight": True,
            }
        expected = {
            "Name": "Horus",
            "Adeptus": "Adeptus Mechanicus",
            "Max wounds": 25,
            "Current wounds": 25,
            "Characteristics": {"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39},
            "Level": (1, "Acolyte"),
            "Skills": {
                "Flee Away": "You retreat to the previous room.",
                "Laser Shot": "Your servo-skull shots a laser beam from its eyes "
                              "dealing (3 + Intellect Bonus) damage."
            },
            "Current experience": 50,
            "Experience for the next level": 1000,
            "Will to fight": True,
            }
        combat(character, enemy={"Name": "Test", "Current wounds": 0, "Will to fight": False, "Experience": 50})
        actual = character
        self.assertEqual(expected, actual)

    @patch('builtins.input', return_value="1")
    def test_combat_will_to_fight_is_set_to_true(self, _):
        character = {
            "Name": "Horus",
            "Adeptus": "Adeptus Mechanicus",
            "Max wounds": 25,
            "Current wounds": 25,
            "Characteristics": {"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39},
            "Level": (1, "Acolyte"),
            "Skills": {
                "Flee Away": "You retreat to the previous room.",
                "Laser Shot": "Your servo-skull shots a laser beam from its eyes "
                              "dealing (3 + Intellect Bonus) damage."
            },
            "Current experience": 0,
            "Previous coordinates": (0, 0),
            "Experience for the next level": 1000,
            "Will to fight": False,
        }
        expected = {
            "Name": "Horus",
            "Adeptus": "Adeptus Mechanicus",
            "Max wounds": 25,
            "Current wounds": 25,
            "Characteristics": {"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39},
            "Level": (1, "Acolyte"),
            "Skills": {
                "Flee Away": "You retreat to the previous room.",
                "Laser Shot": "Your servo-skull shots a laser beam from its eyes "
                              "dealing (3 + Intellect Bonus) damage."
            },
            "Current experience": 0,
            "Previous coordinates": (0, 0),
            "Experience for the next level": 1000,
            "Will to fight": True,
            "X-coordinate": 0,
            "Y-coordinate": 0
        }
        combat(character, enemy={"Name": "Test", "Current wounds": 0, "Will to fight": False, "Experience": 50})
        actual = character
        self.assertEqual(expected, actual)
