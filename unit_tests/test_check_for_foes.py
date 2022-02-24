from unittest import TestCase
from game import check_for_foes as check_for_foes
from unittest.mock import patch


class TestAdd(TestCase):

    @patch('random.randrange', return_value=0)
    def test_check_for_foes_there_is_a_foe(self, _):
        expected = True
        actual = check_for_foes()
        self.assertEqual(expected, actual)

    @patch('random.randrange', side_effect=[1, 2, 3])
    def test_check_for_foes_there_is_no_foe(self, _):
        expected = False
        actual = check_for_foes()
        self.assertEqual(expected, actual)