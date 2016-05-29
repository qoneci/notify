import unittest
from notify.core import validator


class TestSlack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_notify_event_slack(self):
        resp_dict = {
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack'],
            'channel_name': 'test',
        }
        check = validator.notify_event(resp_dict, services=['slack'])
        print(check)
        self.assertNotIn(False, check.values())

    def test_notify_event_slack_datadog(self):
        resp_dict = {
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack'],
            'channel_name': 'test',
            'alert_type': 'info',
            'tags': ['testing:test'],
        }
        check = validator.notify_event(resp_dict, services=['slack', 'datadog'])
        print(check)
        self.assertNotIn(False, check.values())

    def test_notify_event_slack_datadog_invalid_resp(self):
        resp_dict = {
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack'],
            'channel_name': 'test',
        }
        check = validator.notify_event(resp_dict, services=['slack', 'datadog'])
        print(check)
        self.assertIn(False, check.values())
