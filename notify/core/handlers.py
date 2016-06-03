#!/usr/bin/env python3
import asyncio
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

    async def call_slack(self, doc):
        slack_client = Slack(doc.get('org_name'))
        slack_client.init_client()
        await slack_client.send_message(
            doc.get('channel_name'),
            doc.get('message')
        )

    async def call_datadog(self, doc):
        dd = DataDog(doc.get('org_name'))
        dd.init_client()
        await dd.send_event(
            doc.get('alert_type'),
            doc.get('message'),
            tags=doc.get('tags'),
            alert_type=doc.get('alert_type'),
        )

    async def send_events(self, doc, services):
        call_list = []
        if 'slack' in services:
            call_list.append(self.call_slack(doc))
        if 'datadog' in services:
            call_list.append(self.call_datadog(doc))

        await asyncio.wait(call_list)

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
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.send_events(doc, services))

            else:
                raise falcon.HTTPBadRequest('Checks failed {}'.format(checks))
        else:
            raise falcon.HTTPBadRequest('Missing Service in doc {}'.format(doc))

        resp.status = falcon.HTTP_201
