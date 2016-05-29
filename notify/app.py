#!/usr/bin/env python3
import falcon
from notify.core import handlers


api = falcon.API()
api.add_route('/health', handlers.GetHealth())
api.add_route('/api/notify', handlers.NotifyEvent())
