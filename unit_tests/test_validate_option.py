from unittest import TestCase
from game import validate_option as validate_option


class TestAdd(TestCase):

    def test_validate_move_move_is_not_valid_choice_is_numeric_string_and_in_range_of_available_directions_length(self):
        choice = "1"
        available_directions = ["south", "east"]
        expected = True
        actual = validate_option(choice, available_directions)
        self.assertEqual(expected, actual)

    def test_validate_move_is_not_valid_choice_is_alphabetic_string(self):
        choice = "I like doing unit tests"
        available_directions = ["Deadly Burst", "Deus ex Machina"]
        expected = False
        actual = validate_option(choice, available_directions)
        self.assertEqual(expected, actual)

    def test_validate_move_move_is_invalid_choice_is_negative_float(self):
        choice = "-1.5"
        available_directions = ["yes", "no"]
        expected = False
        actual = validate_option(choice, available_directions)
        self.assertEqual(expected, actual)

    def test_validate_move_move_is_invalid_choice_is_not_in_range_of_available_directions_length(self):
        choice = "10"
        available_directions = ["south", "east", "north", "west"]
        expected = False
        actual = validate_option(choice, available_directions)
        self.assertEqual(expected, actual)