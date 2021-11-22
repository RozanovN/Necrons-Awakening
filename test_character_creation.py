from unittest import TestCase
from game import character_creation as character_creation
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.set_name', return_value="Horus")
    @patch('game.set_adeptus', return_value="Adeptus Mechanicus")
    @patch('game.get_skills', return_value="")
    @patch('builtins.input', return_value="1")
    def test_character_creation_test_return(self, _, __, ___):
        expected = {
            "Name": "Horus",
            "Adeptus": "Adeptus Mechanicus",
            "Max wounds": 25,
            "Current wounds": 25,
            "Characteristics": {"Intellect": 50, "Strength": 42, "Toughness": 47, "Agility": 39},
            "Level": [1, "Acolyte"],
            "Skills": {
                "Flee Away": "You retreat to the previous room.",
                "Laser Shot": "Lorem"
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
