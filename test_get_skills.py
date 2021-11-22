from unittest import TestCase
from game import get_skills as get_skills


class Test(TestCase):

    def test_get_command_list(self):
        character = {"Skills": {}, "Adeptus": "Adeptus Astra Telepathica"}
        expected = {"Skills": {"Lightning": "A bolt of blinding lightning strikes from your hand dealing 2k10 damage."},
                    "Adeptus": "Adeptus Astra Telepathica"}
        get_skills(character)
        actual = character
        self.assertEqual(expected, actual)
