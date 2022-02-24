from unittest import TestCase
from game import robotic_wrath as robotic_wrath
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.roll', return_value=5)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_robotic_wrath_print_statement(self, mock_stdout, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = "\n\"TRACEBACK (MOST RECENT CALL LAST):\nFILE ROOT/SERVITOR/BRAIN/COMBAT/ATTACK.py LINE 42, IN " \
                   "<module>\n"\
                   "ZERO DIVISION ERROR: DIVISION BY ZERO\n"\
                   "[FINISHED IN 0.314s WITH EXIT CODE ROBOTIC WRATH],\" your Servitor roars robotically."\
                   "\nThe enraged servitor destroys everything in the way dealing 9 damage to Test.\n"
        robotic_wrath(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.roll', return_value=5)
    def test_robotic_wrath_return_value(self, _):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 9
        actual = robotic_wrath(character, enemy)
        self.assertEqual(expected, actual)
