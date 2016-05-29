#!/usr/bin/env python3
import falcon
from notify.core import handlers
from notify.core.middleware import JSONTranslator, RequireJSON


api = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])


api = falcon.API()
api.add_route('/health', handlers.GetHealth())
api.add_route('/api/notify', handlers.NotifyEvent())
