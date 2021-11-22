from unittest import TestCase
from game import rampage as rampage
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_rampage_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = "\nChar makes a series of bloodthirsty slashes dealing 5 damage to Test.\n"
        rampage(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_rampage_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = 5
        actual = rampage(character, enemy)
        self.assertEqual(expected, actual)
