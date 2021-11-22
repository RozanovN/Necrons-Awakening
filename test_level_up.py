from unittest import TestCase
from game import level_up as level_up
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_level_up_print_statement(self, mock_stdout):
        character = {"Name": "Char", "Current wounds": 25, "Max wounds": 25, "Level": [1, "Acolyte"],
                     "Experience for the next level": 1000, "Skills": {}, "Adeptus": "Adeptus Astra Telepathica",
                     "Current experience": 1200}
        expected = ("\nYou reached new level!\n"
                    "You have got a new skill: Spontaneous Combustion. \n"
                    "The power of your mind ignites your enemy dealing (Bonus Intellect)k10 damage. \n" 
                    "You have now 28 wounds.\n"
                    "\nLevel: 2, Inquisitor\n"
                    "Experience: 1200/2000")
        level_up(character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    def test_level_up_level_2(self):
        character = {"Name": "Char", "Current wounds": 25, "Max wounds": 25, "Level": [1, "Acolyte"],
                     "Experience for the next level": 1000, "Skills": {}, "Adeptus": "Adeptus Astra Telepathica",
                     "Current experience": 1200}
        expected = {"Name": "Char", "Current wounds": 28, "Max wounds": 28, "Level": [2, "Inquisitor"],
                     "Experience for the next level": 2000, "Skills":
                        {"Spontaneous Combustion": "The power of your mind ignites your enemy dealing "
                                                   "(Bonus Intellect)k10 damage"},
                    "Adeptus": "Adeptus Astra Telepathica",
                     "Current experience": 1200}
        level_up(character)
        actual = character
        self.assertEqual(expected, actual)

    def test_level_up_level_3(self):
        character = {"Name": "Char", "Current wounds": 25, "Max wounds": 25, "Level": [2, "Inquisitor"],
                     "Experience for the next level": 2000, "Skills": {}, "Adeptus": "Adeptus Astra Telepathica",
                     "Current experience": 2200}
        expected = {"Name": "Char", "Current wounds": 28, "Max wounds": 28, "Level": [3, "Magister Telepathicae"],
                    "Experience for the next level": "Reached the maximum level", "Skills":
                        {"Chaos of Warp": "One is always equal in death. You make your enemy's wounds equal to yours"},
                    "Adeptus": "Adeptus Astra Telepathica",
                    "Current experience": 2200}
        level_up(character)
        actual = character
        self.assertEqual(expected, actual)
