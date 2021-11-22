from unittest import TestCase
from game import event_with_effect as event_with_effect
from unittest.mock import patch
import io


class Test(TestCase):

    @patch('random.choice', return_value=("Nothing", "Nothing happens"))
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_event_with_effect_check_effect_description(self, mock_stdout, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5}
        expected = "Nothing happens"
        effects = []
        event_with_effect(effects, character)
        actual = mock_stdout.getvalue()
        self.assertEqual(expected + "\n", actual)

    @patch('random.choice', return_value=("Heal", "Heal effect"))
    def test_event_with_effect_check_effect_heal(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 5, "Current experience": 5}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5}
        effects = []
        event_with_effect(effects, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('game.has_evaded', return_value=False)
    @patch('game.has_sustained', return_value=False)
    @patch('builtins.input', return_value="1")
    @patch('random.choice', return_value=("Damage", "Damage test"))
    def test_event_with_effect_check_effect_damage(self, _, __, ___, ____):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 6, "Current experience": 5}
        effects = []
        event_with_effect(effects, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('random.choice', return_value=("Experience gain", "Experience gain test"))
    def test_event_with_effect_check_effect_experience(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 55}
        effects = []
        event_with_effect(effects, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('random.choice', return_value=("Random Stat Deterioration", "Random Stat Deterioration test"))
    def test_event_with_effect_check_effect_stat_decrease(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5,
                     "Characteristics": {("Random Stat Deterioration", "Random Stat Deterioration test"): 25}}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5,
                    "Characteristics": {("Random Stat Deterioration", "Random Stat Deterioration test"): 23}}
        effects = []
        event_with_effect(effects, character)
        actual = character
        self.assertEqual(expected, actual)

    @patch('random.choice', return_value=("Random Stat Improvement", "Random Stat Improvement test"))
    def test_event_with_effect_check_effect_stat_improvement(self, _):
        character = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5,
                     "Characteristics": {("Random Stat Improvement", "Random Stat Improvement test"): 23}}
        expected = {"Name": "Char", "Max wounds": 10, "Current wounds": 10, "Current experience": 5,
                    "Characteristics": {("Random Stat Improvement", "Random Stat Improvement test"): 25}}
        effects = []
        event_with_effect(effects, character)
        actual = character
        self.assertEqual(expected, actual)