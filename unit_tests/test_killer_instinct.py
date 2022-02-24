from unittest import TestCase
from game import killer_instinct as killer_instinct
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_killer_instinct_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYou spray a fan of venomous knives dealing dealing 5 damage to Test.\n"
        killer_instinct(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_killer_instinct_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = 5
        actual = killer_instinct(character, enemy)
        self.assertEqual(expected, actual)
