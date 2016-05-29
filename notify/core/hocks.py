#!/usr/bin/env python3
import json
import falcon


def json_translator(req, resp, resource, params):
    # req.stream corresponds to the WSGI wsgi.input environ variable,
    # and allows you to read bytes from the request body.
    #
    # See also: PEP 3333
    if req.content_length in (None, 0):
        # Nothing to do
        print('JSONTranslato: req.content_length in (None, 0)')
        return

    body = req.stream.read()
    if not body:
        raise falcon.HTTPBadRequest('Empty request body',
                                    'A valid JSON document is required.')

    try:
        req.context['doc'] = json.loads(body.decode('utf-8'))
        print('JSONTranslator: context: {}'.format(req.context))

    except (ValueError, UnicodeDecodeError):
        raise falcon.HTTPError(falcon.HTTP_753,
                               'Malformed JSON',
                               'Could not decode the request body. The '
                               'JSON was incorrect or not encoded as '
                               'UTF-8.')


def require_json(req, resp, resource, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable('This API only supports responses encoded as JSON.')

    if req.method in ('POST', 'PUT'):
        if 'application/json' not in req.content_type:
            raise falcon.HTTPUnsupportedMediaType('This API only supports requests encoded as JSON.')
