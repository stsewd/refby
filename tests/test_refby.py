import unittest
import refby.refby as refby


class TestRefby(unittest.TestCase):

    def setUp(self):
        pass

    def test_public_user_krysthyan09(self):
        self.assertEqual(refby.get_user_id('krysthyan09'), '100009719676455')

    def test_public_user_pedropolisdo(self):
        self.assertEqual(refby.get_user_id('pedropolisdo'), '1202200477')
