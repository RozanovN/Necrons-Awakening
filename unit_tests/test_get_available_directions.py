from unittest import TestCase
from game import get_available_directions as get_available_directions


class TestAdd(TestCase):

    def test_get_available_directions_x_and_y_coordinates_are_zeros(self):
        character = {"X-coordinate": 0, "Y-coordinate": 0, "Current HP": 5}
        rows = 4
        columns = 4
        expected = ["south", "east"]
        actual = get_available_directions(character, columns, rows)
        self.assertEqual(expected, actual)

    def test_get_available_directions_x_coordinate_is_zero_y_coordinate_is_final_y_coordinate(self):
        character = {"X-coordinate": 0, "Y-coordinate": 2, "Current HP": 5}
        rows = 4
        columns = 4
        expected = ["north", "south", "east"]
        actual = get_available_directions(character, columns, rows)
        self.assertEqual(expected, actual)

    def test_get_available_directions_y_coordinate_is_zero_x_coordinate_is_not_final_x_coordinate(self):
        character = {"X-coordinate": 2, "Y-coordinate": 0, "Current HP": 5}
        rows = 4
        columns = 4
        expected = ["south", "west", "east"]
        actual = get_available_directions(character, columns, rows)
        self.assertEqual(expected, actual)

    def test_get_available_directions_all_directions_are_available(self):
        character = {"X-coordinate": 2, "Y-coordinate": 2, "Current HP": 5}
        rows = 4
        columns = 4
        expected = ["north", "south", "west", "east"]
        actual = get_available_directions(character, columns, rows)
        self.assertEqual(expected, actual)

    def test_get_available_directions_x_and_y_coordinates_are_equal_to_final_x_and_y_coordinates(self):
        character = {"X-coordinate": 3, "Y-coordinate": 3, "Current HP": 5}
        rows = 4
        columns = 4
        expected = ["north", "west"]
        actual = get_available_directions(character, columns, rows)
        self.assertEqual(expected, actual)