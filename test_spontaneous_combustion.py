from unittest import TestCase
from game import spontaneous_combustion as spontaneous_combustion
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_spontaneous_combustion_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = "\nThe power of your mind ignites Test dealing 5 damage."
        spontaneous_combustion(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_spontaneous_combustion_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 5
        actual = spontaneous_combustion(character, enemy)
        self.assertEqual(expected, actual)
