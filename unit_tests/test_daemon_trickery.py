from unittest import TestCase
from game import daemon_trickery as daemon_trickery
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=2)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_deadly_burst_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = "\nTest dirtily makes another attack\n\n\nTest deals 10 damage to Char\n"
        daemon_trickery(enemy, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=2)
    def test_deadly_burst_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Agility": 40}}
        enemy = {"Name": "Test"}
        expected = 10
        actual = daemon_trickery(character, enemy)
        self.assertEqual(expected, actual)
