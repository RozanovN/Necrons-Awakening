from unittest import TestCase
from game import charge as charge
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_charge_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = "\nChar's enormous body charges into Test dealing 12 damage\n"
        charge(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_charge_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Strength": 40}}
        enemy = {"Name": "Test"}
        expected = 12
        actual = charge(character, enemy)
        self.assertEqual(expected, actual)
