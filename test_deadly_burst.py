from unittest import TestCase
from game import deadly_burst as deadly_burst
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_deadly_burst_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYou give Test a burst of fire from two plasma-pistols dealing 11 damage.\n"
        deadly_burst(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_deadly_burst_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = 11
        actual = deadly_burst(character, enemy)
        self.assertEqual(expected, actual)
