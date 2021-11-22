from unittest import TestCase
from game import lightning as lightning
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_lightning_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = "\nA bolt of blinding lightning strikes from Char's hand dealing 5 damage to Test."
        lightning(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_lightning_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = 5
        actual = lightning(character, enemy)
        self.assertEqual(expected, actual)
