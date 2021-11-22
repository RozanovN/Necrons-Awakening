from unittest import TestCase
from game import character_creation as character_creation
from unittest.mock import patch


class Test(TestCase):

    @patch('game.set_name', return_value="Horus")
    @patch('game.set_adeptus', return_value="Adeptus Mechanicus")
    @patch('game.set_wounds', return_value=25)
    @patch('game.get_characteristics', return_value={"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39})
    @patch('game.get_level_name', return_value=(1, "Acolyte"))
    @patch('builtins.input', return_value="1")
    def test_character_creation_test_whether_valid_character_returned(self, _, __, ___, ____, _____, ______):
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
            "X-coordinate": 0,
            "Y-coordinate": 0,
            "Previous coordinates": (0, 0),
            "Current experience": 0,
            "Experience for the next level": 1000,
            "Will to fight": True,
            "Inventory": {
                "Bandage": 10,
                "Torch": 10
            }
        }
        actual = character_creation()
        self.assertEqual(expected, actual)
