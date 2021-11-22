from unittest import TestCase
from game import has_evaded as has_evaded
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_has_evaded_check_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60}}
        expected = "[1;32m----------------------------------Evasion Check---------------------------------" \
                   "----------------------[0;20m"
        has_evaded(character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=100)
    def test_has_evaded_unsuccessful_return_value_(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60}}
        expected = False
        actual = has_evaded(character)
        self.assertEqual(expected, actual)

    @patch('game.roll', return_value=5)
    def test_has_evaded_successful_return_value_(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40, "Agility": 60}}
        expected = True
        actual = has_evaded(character)
        self.assertEqual(expected, actual)
