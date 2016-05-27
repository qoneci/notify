#!/usr/bin/env python3
from logbook import Logger, StreamHandler
import sys


LOG_BASE = 'notify'


def logger():
    StreamHandler(sys.stdout).push_application()
    return Logger(LOG_BASE)
