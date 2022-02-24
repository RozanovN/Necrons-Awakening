from unittest import TestCase
from game import laser_shot as laser_shot
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_laser_shot_print_statement(self, mock_stdout):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = "\nYour servo-skull shots a laser beam from its eyes dealing 7 damage to Test.\n"
        laser_shot(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    def test_laser_shot_return_value(self):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 7
        actual = laser_shot(character, enemy)
        self.assertEqual(expected, actual)
