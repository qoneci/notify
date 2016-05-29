#!/usr/bin/env python3
import falcon
from notify.core.log import logger
from notify.plugins import services


class GetHealth:
    def __init__(self):
        self.log = logger()

    def on_get(self, req, resp):
        resp.body = '{"status": "OK"}'


class NotifyEvent:
    def __init__(self):
        self.log = logger()

    def on_post(self, req, resp):
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest('must be submitted in the request body.')

        resp.status = falcon.HTTP_201
