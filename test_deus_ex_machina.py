from unittest import TestCase
from game import deus_ex_machina as deus_ex_machina
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_deadly_burst_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYou give Test a burst of fire from two plasma-pistols dealing 11 damage.\n"
        deus_ex_machina(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_deadly_burst_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = 11
        actual = deus_ex_machina(character, enemy)
        self.assertEqual(expected, actual)
