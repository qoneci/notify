import unittest
from notify.core import config_parser


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = config_parser.ConfLoader()
        cls.file_path = 'tests/test_notify.yml'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validate_slack(self):
        yml = {'slack': {'orgs': [{'name': '', 'token': ''}]}}
        check = self.loader._validate_slack(yml)
        self.assertTrue(check)

    def test_validate_hipchat(self):
        yml = {'hipchat': {'orgs': [{'name': '', 'token': ''}]}}
        check = self.loader._validate_hipchat(yml)
        self.assertTrue(check)

    def test_validate_datadog(self):
        yml = {'datadog': {'orgs': [{'name': '', 'token': ''}]}}
        check = self.loader._validate_datadog(yml)
        self.assertTrue(check)

    def test_slack_config(self):
        conf = self.loader.get_config('slack', file_path=self.file_path)
        self.assertIn('token', conf['slack']['orgs'][0].keys())
        self.assertIn('name', conf['slack']['orgs'][0].keys())

    def test_hipchat_config(self):
        conf = self.loader.get_config('hipchat', file_path=self.file_path)
        self.assertIn('token', conf['hipchat']['orgs'][0].keys())
        self.assertIn('name', conf['hipchat']['orgs'][0].keys())

    def test_datadog_config(self):
        conf = self.loader.get_config('datadog', file_path=self.file_path)
        self.assertIn('token', conf['datadog']['orgs'][0].keys())
        self.assertIn('name', conf['datadog']['orgs'][0].keys())
