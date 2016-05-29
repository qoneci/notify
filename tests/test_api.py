import json
import requests
import unittest
import falcon
import falcon.testing as testing

from notify.core import handlers
from notify.core.middleware import JSONTranslator, RequireJSON


class TestAPI(testing.TestBase):
    def before(self):
        # TestBase provides an instance of falcon.API to use along
        # with simulate_request (see below).
        self.api = falcon.API(middleware=[RequireJSON(), JSONTranslator()])
        self.api.add_route('/health', handlers.GetHealth())
        self.api.add_route('/api/notify', handlers.NotifyEvent())

    def test_get_health(self):
        # TestBase provides a method to simulate a WSGI request without
        # having to stand up an actual server. The decode option tells
        # simulate_request to convert the raw WSGI response into a
        # Unicode string.
        body = self.simulate_request('/health', decode='utf-8')

        # TestBase provides an instance of StartResponseMock that captures
        # the data passed to WSGI's start_response callback. This includes
        # the status code and headers returned by the Falcon app.
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        json_body = json.loads(body)
        self.assertEqual(json_body, {'status': 'OK'})

    '''
    def test_post_slack_event(self):
        body = json.dumps({
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack'],
            'channel_name': 'test',
        })
        headers = {'content-type': 'application/json'}
        self.simulate_request(
            '/api/notify',
            method='POST',
            decode='utf-8',
            headers=headers,
            body=body
        )
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

    def test_post_multi_event(self):
        body = json.dumps({
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack', 'datadog'],
            'channel_name': 'test',
            'alert_type': 'info',
            'tags': ['testing:test'],
        })
        headers = {'content-type': 'application/json'}
        self.simulate_request(
            '/api/notify',
            method='POST',
            decode='utf-8',
            headers=headers,
            body=body
        )
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
    '''

    def test_post_event_invalid_json_body(self):
        body = str({'alert_type': 'info', 'tags': ['testing:test']})
        headers = {'content-type': 'application/json'}
        self.simulate_request(
            '/api/notify',
            method='POST',
            decode='utf-8',
            headers=headers,
            body=body
        )
        self.assertEqual(self.srmock.status, falcon.HTTP_753)


class TestAPIIntergartionTesting(unittest.TestCase):

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

    def test_post_multi_event(self):
        body = json.dumps({
            'org_name': 'qoneci',
            'message': 'foo bar',
            'services': ['slack', 'datadog'],
            'channel_name': 'test',
            'alert_type': 'info',
            'tags': ['testing:test'],
        })
        headers = {'content-type': 'application/json'}
        resp = requests.post('http://localhost:8000/api/notify', headers=headers, data=body)
        print(resp.text)
        self.assertEqual(resp.status_code, 201)
