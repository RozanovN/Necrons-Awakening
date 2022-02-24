from unittest import TestCase
from game import enemy_attack as enemy_attack
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_enemy_attack_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "rat", "Skills": {"Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)}}
        expected = "\nThe rat greedily bites you with its front teeth dealing 5 damage to Char.\n"
        enemy_attack(enemy, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_enemy_attack_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "rat", "Skills": {"Enemy Attack": ("The rat greedily bites you with its front teeth", 1, 5)}}
        expected = 5
        actual = enemy_attack(enemy, character)
        self.assertEqual(expected, actual)
