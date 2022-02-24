from unittest import TestCase
from game import manage_events as manage_events
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('random.choice', return_value="This is entrance")
    @patch('builtins.input', return_value="1")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_manage_events_description(self, mock_stdout, _, __):
        character = {"Y-coordinate": 0, "X-coordinate": 0}
        board = {(0, 0): "Entrance"}
        expected = "\nThis is entrance\n"\
                   "Time to move.\n"\
                   "[1;32m\n"\
                   "Enter anything to continue:[0;20m"
        manage_events(board, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)
