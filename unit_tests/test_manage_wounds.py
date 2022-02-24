from unittest import TestCase
from game import manage_wounds as manage_wounds
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('game.has_evaded', return_value=True)
    @patch('builtins.input', return_value="1")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_manage_wounds_has_evaded_print_statement(self, mock_stdout, _, __):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = "[1;32mHowever, abc evades it.[0;20m\n"\
                   "[1;32m\n"\
                   "Enter anything to continue:[0;20m"
        manage_wounds(damage, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.has_evaded', return_value=False)
    @patch('game.has_sustained', return_value=True)
    @patch('builtins.input', return_value="1")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_manage_wounds_has_sustained_print_statement(self, mock_stdout, _, __, ___):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = "[1;31mAbc was not able to evade.[0;20m\n" \
                   "[1;32mHowever, abc sustains it and only receives 2 damage.[0;20m\n"\
                   "[1;32m\n" \
                   "Enter anything to continue:[0;20m"
        manage_wounds(damage, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.has_evaded', return_value=False)
    @patch('game.has_sustained', return_value=False)
    @patch('builtins.input', return_value="1")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_manage_wounds_full_damage_statement(self, mock_stdout, _, __, ___):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = "[1;31mAbc was not able to evade.[0;20m\n" \
                   "[1;31mAbc was not able to sustain.[0;20m\n"\
                   "[1;32m\n" \
                   "Enter anything to continue:[0;20m"
        manage_wounds(damage, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('game.has_evaded', return_value=True)
    @patch('game.has_sustained', return_value=False)
    @patch('builtins.input', return_value="1")
    def test_manage_wounds_has_evaded_wounds_are_not_changed(self, _, __, ___):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = {"Name": "abc", "Current wounds": 5}
        manage_wounds(damage, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('game.has_evaded', return_value=False)
    @patch('game.has_sustained', return_value=True)
    @patch('builtins.input', return_value="1")
    def test_manage_wounds_has_sustain_receives_half_of_damage(self, _, __, ___):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = {"Name": "abc", "Current wounds": 3}
        manage_wounds(damage, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('game.has_evaded', return_value=False)
    @patch('game.has_sustained', return_value=False)
    @patch('builtins.input', return_value="1")
    def test_manage_wounds_full_damage_receives_full_damage(self, _, __, ___):
        character = {"Name": "abc", "Current wounds": 5}
        damage = 5
        expected = {"Name": "abc", "Current wounds": 0}
        manage_wounds(damage, character)
        actual = character
        self.assertEqual(expected, actual)
