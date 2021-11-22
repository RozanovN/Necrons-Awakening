from unittest import TestCase
from game import get_map as get_map


class Test(TestCase):

    def test_get_map(self):
        expected = "🚪\t☐\t*\t*\t*\t\n*\t✙\t*\t*\t*\t\n*\t*\t\x1b[1;32mU\x1b[0;20m\t*\t*\t\n*\t*\t*\t*\t*\t\n*\t*" \
                   "\t*\t*\t*\t\n"
        actual = get_map({(0, 0): "Entrance", (0, 1): "Empty Room", (1, 1): "Ancient Altar Room"},
                         {"Y-coordinate": 2,"X-coordinate": 2}, 5, 5)
        self.assertEqual(expected, actual)
