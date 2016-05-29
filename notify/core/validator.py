import cerberus


def get_schema_by_service(service):
    schema1 = {
        'org_name': {'type': 'string', 'required': True},
        'message': {'type': 'string', 'required': True},
        'services': {'type': 'list', 'required': True},
        'channel_name': {'type': 'string', 'required': True},
        'tags': {'type': 'list'},
        'alert_type': {
            'type': 'string', 'allowed': ['error', 'warning', 'info', 'success']
        },
    }

    schema2 = {
        'org_name': {'type': 'string', 'required': True},
        'message': {'type': 'string', 'required': True},
        'services': {'type': 'list', 'required': True},
        'channel_name': {'type': 'string', 'required': True},
        'tags': {'type': 'list', 'required': True},
        'alert_type': {
            'type': 'string', 'required': True, 'allowed': ['error', 'warning', 'info', 'success']
        },
    }
    if service in ['hipchat', 'slack']:
        return schema1
    elif service in ['datadog']:
        return schema2
    else:
        return {}


def notify_event(resp_dict, services=list):
    result = {}
    for i in services:
        schema = get_schema_by_service(i)
        check = cerberus.Validator(schema).validate(resp_dict)
        result.update({i: check})
    return result
