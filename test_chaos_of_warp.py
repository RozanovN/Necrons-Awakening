from unittest import TestCase
from game import chaos_of_warp as chaos_of_warp


class Test(TestCase):

    def test_chaos_of_warp_enemy_max_wounds_are_equal_to_character_max_wounds(self):
        character = {"Name": "Test", "Current wounds": 1, "Max wounds": 1}
        enemy = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 100,
                 "Max wounds": 100}
        expected = {"Name": "Goreclaw the Render, a Daemon Prince of Khorne", "Current wounds": 1,
                    "Max wounds": 1}
        chaos_of_warp(character, enemy)
        actual = enemy
        self.assertEqual(expected, actual)
