from unittest import TestCase
from game import colossus_smash as colossus_smash
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_colossus_smash_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = "\nA devastating blow of Char weapon rips and tears Test dealing 9 damage\n"
        colossus_smash(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_colossus_smash_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = 9
        actual = colossus_smash(character, enemy)
        self.assertEqual(expected, actual)
