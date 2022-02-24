from unittest import TestCase
from game import deus_ex_machina as deus_ex_machina
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('random.choices', return_value=["Laser Shot", "Robotic Wrath", "Laser Shot"])
    @patch('game.roll', return_value=3)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_deadly_burst_print_statement(self, mock_stdout, _, __):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = ("\nYou pray Omnissiah to slay fools who cannot see the stupor mundi of machines.\n\n"
                    "\nYour servo-skull shots a laser beam from its eyes dealing 7 damage to Test.\n\n"
                    "\n\"TRACEBACK (MOST RECENT CALL LAST):\nFILE ROOT/SERVITOR/BRAIN/COMBAT/ATTACK.py LINE 42, IN "
                    "<module>\n"
                    "ZERO DIVISION ERROR: DIVISION BY ZERO\n"
                    "[FINISHED IN 0.314s WITH EXIT CODE ROBOTIC WRATH],\" your Servitor roars robotically."
                    "\nThe enraged servitor destroys everything in the way dealing 7 damage to Test.\n\n"
                    "\nYour servo-skull shots a laser beam from its eyes dealing 7 damage to Test.\n")
        deus_ex_machina(character, enemy)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('random.choices', return_value=["Laser Shot", "Robotic Wrath", "Laser Shot"])
    @patch('game.roll', return_value=3)
    def test_deadly_burst_return_value(self, _, __):
        character = {"Name": "Char", "Characteristics": {"Intellect": 40}}
        enemy = {"Name": "Test"}
        expected = 21
        actual = deus_ex_machina(character, enemy)
        self.assertEqual(expected, actual)
