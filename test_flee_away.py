from unittest import TestCase
from game import flee_away as flee_away
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_flee_away_damageless_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60}, "Skills": {"Laser Shot": 1}}
        enemy = {"Name": "rat", "Characteristics": {"Agility": 60},
                 "Skills": {"Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)}}
        expected = ("[1;32m----------------------------------------Fleeing------------------------------------------"
                    "-------------[0;20m\n\n[1;32mChar decides to flee away.[0;20m\nChar flees without damage."
                    )
        flee_away(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=100)
    @patch('builtins.input', return_value="1")
    @patch('game.manage_wounds', return_value=100)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_flee_away_damage_is_received_print_statement(self, mock_stdout, _, __, ___):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60, "Toughness": 60},
                     "Skills": {"Laser Shot": 1}, "Current wounds": 200}
        enemy = {"Name": "rat", "Characteristics": {"Agility": 60},
                 "Skills": {"T": "Test", "Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)}}
        expected = ("[1;32m----------------------------------------Fleeing------------------------------------------"
                    "-------------[0;20m\n\n[1;32mChar decides to flee away.[0;20m\nChar is not quick enough "
                    "to flee without damage.\n\n"
                    "The rat greedily bites you with its front teeth dealing 100 damage to Char.\n")
        flee_away(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_flee_away_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60}, "Skills": {"Laser Shot": 1}}
        enemy = {"Name": "rat", "Characteristics": {"Agility": 60},
                 "Skills": {"Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)}}
        expected = 0
        actual = flee_away(enemy, character)
        self.assertEqual(expected, actual)
