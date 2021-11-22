from unittest import TestCase
from game import boss as boss
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_boss_level_is_not_three_print_statement(self, mock_stdout):
        character = {"Name": "Test", "Skills": {"Flee Away"}, "Level": (1, "Acolyte"), "Previous coordinates": (1, 0),
                     "X-coordinate": 0, "Y-coordinate": 0}
        expected = ("Fear takes control over you as soon as you get close to this room.\n"
                    "You feel like you have to get more experience before facing it.\nYou decide to retreat.")
        boss(character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.combat', return_value=None)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_boss_level_is_three_print_statement(self, mock_stdout, _):
        character = {"Name": "Test", "Skills": {"Flee Away": "whatever"},
                     "Level": (3, "whatever"), "Previous coordinates": (1, 0),
                     "X-coordinate": 0, "Y-coordinate": 0}
        expected = ("\n\tYou enter the dreadful room. The Necronian decor exactly matches the description "
                    "the Inquisitor gave you"
                    ". However, your joy deserves rapidly as you notice a gigantic\ndaemon holding the precious "
                    "artefact"
                    "you are tasked to retrieve. The daemon notices you and smirks. His grotesque claws reveals his "
                    "name ——"
                    "Goreclaw the Render, a\nDaemon Prince of Khorne —— infamous among the inquisitors of this galaxy."
                    "\n\nYou know it will be a deadly battle with no opportunity to flee."
                    "\n\"Bring. It. On,\" his monstrous majesty mandates")
        boss(character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.combat', return_value=None)
    def test_boss_level_is_three_artefact_is_added(self, _):
        character = {"Name": "Test", "Skills": {"Flee Away": "whatever"},
                     "Level": (3, "whatever"), "Previous coordinates": (1, 0),
                     "X-coordinate": 0, "Y-coordinate": 0}
        expected = {"Name": "Test", "Skills": {},
                     "Level": (3, "whatever"), "Previous coordinates": (1, 0),
                     "X-coordinate": 0, "Y-coordinate": 0, "Artifact": "Necronian artifact"}
        boss(character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('game.combat', return_value=None)
    def test_boss_level_is_three_flee_away_is_removed(self, _):
        character = {"Name": "Yet another Test", "Skills": {"Flee Away": "whatever"},
                     "Level": (3, "whatever"), "Previous coordinates": (1, 0),
                     "X-coordinate": 0, "Y-coordinate": 0}
        expected = {"Name": "Test", "Skills": {},
                    "Level": (3, "whatever"), "Previous coordinates": (1, 0),
                    "X-coordinate": 0, "Y-coordinate": 0, "Artifact": "Necronian artifact"}
        boss(character)
        actual = character
        self.assertEqual(expected, actual)
