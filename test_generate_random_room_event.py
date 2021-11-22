from unittest import TestCase
from game import generate_random_room_event as generate_random_room_event
from unittest.mock import patch


class Test(TestCase):

    @patch('random.choices', return_value=["Shifting Mist"])
    def test_generate_random_room_event(self, _):
        expected = "Shifting Mist"
        actual = generate_random_room_event()
        self.assertEqual(expected, actual)