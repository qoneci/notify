import yaml
import os.path
import cerberus
from yaml import YAMLError
from notify.core.log import logger


class Config(object):
    def __init__(self, conf):
        self.conf = conf

    def get_service(self, service, org_name):
        service_conf = {}
        try:
            service_conf = [x for x in self.conf[service]['orgs'] if x.get('name') == org_name]
        except KeyError:
            pass
        finally:
            return service_conf


class ConfLoader(object):
    def __init__(self):
        self.log = logger()

    def get_schema(self, service):
        schema1 = {
            'orgs': {
                'type': 'list', 'schema': {
                    'type': 'dict', 'schema': {
                        'name': {'type': 'string'},
                        'token': {'type': 'string'},
                        'api_key': {'type': 'string'},
                    }
                }
            }
        }

        if service in ['slack', 'hipchat', 'datadog']:
            return schema1
        else:
            return {}

    def _validate(self, yml, service):
        schema = self.get_schema(service)
        if schema:
            return cerberus.Validator(schema).validate(yml)
        else:
            return False

    def _validate_slack(self, yml):
        slack_conf = yml.get('slack')
        if slack_conf:
            return self._validate(slack_conf, 'slack')
        else:
            return False

    def _validate_hipchat(self, yml):
        hipchat_conf = yml.get('hipchat')
        if hipchat_conf:
            return self._validate(hipchat_conf, 'hipchat')
        else:
            return False

    def _validate_datadog(self, yml):
        datadog_conf = yml.get('datadog')
        if datadog_conf:
            return self._validate(datadog_conf, 'datadog')
        else:
            return False

    def validate_yml(self, yml, plugin_type):
        if plugin_type == 'slack':
            return self._validate_slack(yml)
        elif plugin_type == 'hipchat':
            return self._validate_hipchat(yml)
        elif plugin_type == 'datadog':
            return self._validate_hipchat(yml)

    def _load_file(self, file_path='.notify.yml'):
        yml_file = {}
        if os.path.isfile(file_path):
            with open(file_path, 'r') as stream:
                try:
                    yml_file = yaml.load(stream)
                    self.log.info('ConfLoader.load_file loaded: {}', yml_file)
                except YAMLError as err:
                    self.log.error('ConfLoader.load_file error: {}', err)
                finally:
                    return yml_file
        else:
            self.log.error('ConfLoader.load_file file .notify.yml not found')
            return yml_file

    def get_config(self, plugin_type, file_path='.notify.yml'):
        config_yml = self._load_file()
        if config_yml:
            validate = self.validate_yml(config_yml, plugin_type)
            if validate:
                self.log.info('ConfLoader.get_config: config_yml: {}', config_yml)
                return config_yml
        else:
            self.log.error('ConfLoader.get_config: validate_yml failed')
            return config_yml
