from unittest import TestCase
from game import get_level_name as get_level_name


class Test(TestCase):

    def test_get_level_name_level_is_not_three(self):
        adeptus = "Adeptus Astra Telepathica"
        level = 1
        expected = [1, "Acolyte"]
        actual = get_level_name(adeptus, level)
        self.assertEqual(expected, actual)

    def test_get_level_name_level_is_three(self):
        adeptus = "Adeptus Astra Telepathica"
        level = 3
        expected = [3, "Magister Telepathicae"]
        actual = get_level_name(adeptus, level)
        self.assertEqual(expected, actual)