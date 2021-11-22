from unittest import TestCase
from game import generate_enemy as generate_enemy
from unittest.mock import patch


class Test(TestCase):

    @patch('random.choices', return_value=["the rat"])
    def test_generate_enemy_random_enemy(self, _):
        character = {"Level": (1, "Acolyte")}
        expected = {
                "Name": "the rat",
                "Max wounds": 5,
                "Current wounds": 5,
                "Characteristics": {
                    "Intellect": 10,
                    "Strength": 15,
                    "Toughness": 15,
                    "Agility": 25
                },
                "Skills": {
                    "Flee Away": "The rat flees away.",
                    "Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)
                },
                "Will to fight": True,
                "Experience": 150
            }
        actual = generate_enemy(character["Level"][0])
        self.assertEqual(expected, actual)

    def test_generate_enemy_specific_enemy(self):
        character = {"Level": (1, "Acolyte")}
        expected = {
                "Name": "the rat",
                "Max wounds": 5,
                "Current wounds": 5,
                "Characteristics": {
                    "Intellect": 10,
                    "Strength": 15,
                    "Toughness": 15,
                    "Agility": 25
                },
                "Skills": {
                    "Flee Away": "The rat flees away.",
                    "Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)
                },
                "Will to fight": True,
                "Experience": 150
            }
        actual = generate_enemy(character["Level"][0], "the rat")
        self.assertEqual(expected, actual)
