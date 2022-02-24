from unittest import TestCase
from game import has_sustained as has_sustained
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_has_sustained_check_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Toughness": 60}}
        expected = "[1;32m----------------------------------Toughness Check-------------------------------" \
                   "----------------------[0;20m"
        has_sustained(character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=100)
    def test_has_sustained_unsuccessful_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Toughness": 60}}
        expected = False
        actual = has_sustained(character)
        self.assertEqual(expected, actual)

    @patch('game.roll', return_value=5)
    def test_has_sustained_successful_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Toughness": 60}}
        expected = True
        actual = has_sustained(character)
        self.assertEqual(expected, actual)