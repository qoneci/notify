import unittest
from notify.plugins.services import Slack


class TestSlack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = Slack('qoneio')
        cls.sc.init_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_auth_test(self):
        auth = self.sc._auth_test()
        self.assertTrue(auth.get('ok'))

    def test_api_test(self):
        api = self.sc._api_test()
        self.assertTrue(api.get('ok'))

    def test_list_channels(self):
        result = self.sc.channels_list()
        self.assertTrue(len(result) >= 2)

    def test_channels_and_id(self):
        result = self.sc.channels_names_and_id()
        print(result)
        self.assertIn('general', result.keys())
        self.assertIn('random', result.keys())

    def test_send_message(self):
        channels_map = self.sc.channels_names_and_id()
        result = self.sc.send_message(
            channels_map.get('test'),
            'foo bar'
        )
        self.assertTrue(result.get('ok'))
