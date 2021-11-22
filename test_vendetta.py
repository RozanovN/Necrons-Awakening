from unittest import TestCase
from game import vendetta as vendetta
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_vendetta_print_statement_roll_less_than_20(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYour fatal shot deals 5 damage to Test."\
                   "\nV means very random."
        vendetta(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=25)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_vendetta_print_statement_roll_bigger_than_20(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYour fatal shot deals 25 damage to Test."
        vendetta(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=100)
    def test_vendetta_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 100
        actual = vendetta(character, enemy)
        self.assertEqual(expected, actual)
