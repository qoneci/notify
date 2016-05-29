#!/usr/bin/env python3
import falcon
from notify.core import hocks
from notify.core import validator
from notify.core.log import logger
from notify.plugins.services import Slack
from notify.plugins.services import DataDog


class GetHealth:
    def __init__(self):
        self.log = logger()

    def on_get(self, req, resp):
        resp.body = '{"status": "OK"}'


class NotifyEvent:
    def __init__(self):
        self.log = logger()

    @falcon.before(hocks.require_json)
    @falcon.before(hocks.json_translator)
    def on_post(self, req, resp):
        doc = None
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest('JSONTranslator failed',
                                        'JSON must be submitted in the request body.')

        if isinstance(doc.get('services'), list):
            checks = validator.notify_event(doc, services=doc.get('services'))
            if False not in checks:
                services = doc.get('services')
                if 'slack' in services:
                    slack_client = Slack(doc.get('org_name'))
                    slack_client.init_client()
                    slack_client.send_message(
                        doc.get('channel_name'),
                        doc.get('message')
                    )
                if 'datadog' in services:
                    dd = DataDog(doc.get('org_name'))
                    dd.init_client()
                    dd.send_event(
                        doc.get('alert_type'),
                        doc.get('message'),
                        tags=doc.get('tags'),
                        alert_type=doc.get('alert_type'),
                    )
            else:
                raise falcon.HTTPBadRequest('Checks failed {}'.format(checks))
        else:
            raise falcon.HTTPBadRequest('Missing Service in doc {}'.format(doc))

        resp.status = falcon.HTTP_201
