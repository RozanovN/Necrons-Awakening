from unittest import TestCase
from game import move_character as move_character


class TestAdd(TestCase):

    def test_move_character_south(self):
        character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5}
        direction_index = 0
        available_directions = ["south", "east"]
        expected = {"X-coordinate": 0, "Y-coordinate": 1, "Current HP": 5, "Previous coordinates": (0, 0)}
        move_character(character,  direction_index, available_directions)
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_east(self):
        character = {"X-coordinate": 0, "Y-coordinate": 1, "Current HP": 5}
        direction_index = 2
        available_directions = ["north", "south", "east"]
        expected = {"X-coordinate": 1, "Y-coordinate": 1, "Current HP": 5, "Previous coordinates": (1, 0)}
        move_character(character,  direction_index, available_directions)
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_north(self):
        character = {"X-coordinate": 1, "Y-coordinate": 1, "Current HP": 5}
        direction_index = 0
        available_directions = ["north", "south", "west", "east"]
        expected = {"X-coordinate": 1, "Y-coordinate": 0, "Current HP": 5, "Previous coordinates": (1, 1)}
        move_character(character,  direction_index, available_directions)
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_west(self):
        character = {"X-coordinate": 1, "Y-coordinate": 1, "Current HP": 5}
        direction_index = 3
        available_directions = ["north", "south", "east", "west"]
        expected = {"X-coordinate": 0, "Y-coordinate": 1, "Current HP": 5, "Previous coordinates": (1, 1)}
        move_character(character,  direction_index, available_directions)
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_previous_coordinates(self):
        character = {"X-coordinate": 1, "Y-coordinate": 1, "Current HP": 5, "Previous coordinates": (0, 1)}
        direction_index = 3
        expected = {"X-coordinate": 1, "Y-coordinate": 0, "Current HP": 5, "Previous coordinates": (0, 1)}
        move_character(character)
        actual = character
        self.assertEqual(expected, actual)

    def test_move_character_test_return(self):
        character = {"X-coordinate": 1, "Y-coordinate": 1, "Current HP": 5}
        available_directions = ["north", "south", "east", "west"]
        direction_index = 3
        expected = (1, 0)
        actual = move_character(character, direction_index, available_directions)
        self.assertEqual(expected, actual)
