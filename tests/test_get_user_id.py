from unittest import TestCase

import refby.refby as refby
from refby.errors import UserIdNotFoundError
from refby.errors import PrivateOrInvalidProfileError


class TestGetUserId(TestCase):

    def setUp(self):
        pass

    def test_public_user_krysthyan09(self):
        self.assertEqual(refby.get_user_id('krysthyan09'), '100009719676455')

    def test_public_user_pedropolisdo(self):
        self.assertEqual(refby.get_user_id('pedropolisdo'), '1202200477')

    def test_page_billgates(self):
        with self.assertRaises(UserIdNotFoundError):
            refby.get_user_id('billgates')

    def test_invalid_user_asdfdfdal(self):
        with self.assertRaises(PrivateOrInvalidProfileError):
            refby.get_user_id('asdfdfdal')

    def test_private_user_stsewd2(self):
        with self.assertRaises(PrivateOrInvalidProfileError):
            refby.get_user_id('stsewd2')
