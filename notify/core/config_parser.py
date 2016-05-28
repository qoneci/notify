import yaml
import os.path
from yaml import YAMLError
from notify.core.log import logger


class ConfLoader(object):
    def __init__(self):
        self.log = logger()

    def _validate(self, yml, mandatory_keys=list):
        mandatory_keys = mandatory_keys
        missing_keys = []
        orgs = yml.get('orgs')
        for i in orgs:
            missing_keys + [x for x in mandatory_keys if x not in i]

        if missing_keys:
            self.log.error(
                'ConfLoader.validate_yml error: missing keys in yml: {}',
                missing_keys
            )
            print(missing_keys)
            return False
        else:
            self.log.info('ConfLoader.validate_yml Ok!')
            return True

    def _validate_slack(self, yml):
        slack_conf = yml.get('slack')
        if slack_conf:
            return self._validate(yml['slack'], mandatory_keys=['name', 'token'])
        else:
            return False

    def _validate_hipchat(self, yml):
        hipchat_conf = yml.get('hipchat')
        if hipchat_conf:
            return self._validate(yml['hipchat'], mandatory_keys=['name', 'token'])
        else:
            return False

    def _validate_datadog(self, yml):
        datadog_confg = yml.get('datadog')
        if datadog_confg:
            return self._validate(yml['datadog'], mandatory_keys=['name', 'token'])
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
