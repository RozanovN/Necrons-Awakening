from unittest import TestCase
from game import blade_of_chaos as blade_of_chaos
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('itertools.combinations', return_value=["AB"])
    @patch('builtins.input', return_value="AB")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_blade_of_chaos_successful_guess_check_print_statement(self, mock_stdout, _, __):
        character = {"Name": "Test", "Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        expected = (
            "\nYou notice how this fiend of Khorne prepares a slash attack. You have an opportunity to deflect it if"
            " you"
            "guess the 2 body parts he aims for H(head), B(body), A(arms), F(feet). He certainly will not be able to"
            "evade or sustain it."
            "\nEnter the first letters of 2 body parts (AB for arms and body):\n"
            "\nSuccess! You deflect the attack! Who is smirking now? Goreclaw the Render, a Daemon Prince of Khorne "
            "receives 8 damage"
        )
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 10}
        blade_of_chaos(enemy, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('itertools.combinations', return_value=["HA"])
    @patch('builtins.input', return_value="AB")
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_blade_of_chaos_unsuccessful_guess_check_print_statement(self, mock_stdout, _, __):
        character = {"Name": "Test", "Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        expected = (
            "\nYou notice how this fiend of Khorne prepares a slash attack. You have an opportunity to deflect it"
            " if you"
            "guess the 2 body parts he aims for H(head), B(body), A(arms), F(feet). He certainly will not be able to"
            "evade or sustain it."
            "\nEnter the first letters of 2 body parts (AB for arms and body):\n"
            "\nFailure! Goreclaw the Render, a Daemon Prince of Khorne smirks and deals 8 damage to Test."
        )
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 10}
        blade_of_chaos(enemy, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('itertools.combinations', return_value=["AB"])
    @patch('builtins.input', return_value="AB")
    def test_blade_of_chaos_successful_guess_check_damage_is_received_by_boss(self, _, __):
        character = {"Name": "Test", "Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 10}
        expected = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 2}
        blade_of_chaos(enemy, character)
        actual = enemy
        self.assertEqual(expected, actual)

    @patch('itertools.combinations', return_value=["AB"])
    @patch('builtins.input', return_value="AB")
    def test_blade_of_chaos_successful_guess_check_return_is_equal_to_zero(self, _, __):
        character = {"Name": "Test", "Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 10}
        expected = 0
        actual = blade_of_chaos(enemy, character)
        self.assertEqual(expected, actual)

    @patch('itertools.combinations', return_value=["AH"])
    @patch('builtins.input', return_value="AB")
    def test_blade_of_chaos_unsuccessful_guess_check_return_is_equal_to_eight(self, _, __):
        character = {"Name": "Test", "Current wounds": 10, "Max wounds": 20, "Inventory": {"Bandage": 5}}
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 10}
        expected = 8
        actual = blade_of_chaos(enemy, character)
        self.assertEqual(expected, actual)
