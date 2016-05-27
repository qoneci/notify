import yaml
import os.path
from yaml import YAMLError
from notify.core.log import logger


class ConfLoader(object):
    def __init__(self):
        self.log = logger()

    def _validate(self, yml, mandatory_keys=list):
        mandatory_keys = mandatory_keys
        missing_keys = [x for x in mandatory_keys if x not in yml]
        if missing_keys:
            self.log.error(
                'ConfLoader.validate_yml error: missing keys in yml: {}',
                missing_keys
            )
            return False
        else:
            self.log.info('ConfLoader.validate_yml Ok!')
            return True

    def _validate_slack(self, yml):
        slack_conf = yml.get('slack')
        if slack_conf:
            return self._validate(yml, mandatory_keys=['name', 'token'])

    def _validate_hipchat(self, yml):
        hipchat_conf = yml.get('hipchat')
        if hipchat_conf:
            return self._validate(yml, mandatory_keys=['name', 'token'])

    def _validate_datadog(self, yml):
        datadog_confg = yml.get('datadog')
        if datadog_confg:
            return self._validate(yml, mandatory_keys=['name', 'token'])

    def validate_yml(self, yml, plugin_type):
        pass

    def _load_file(self):
        yml_file = {}
        file_path = '.notify.yml'
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

    def get_config(self, plugin_type):
        config_yml = self._load_file()
        if config_yml:
            validate = self.validate_yml()
            if validate:
                self.log.info('ConfLoader.get_config: config_yml: {}', config_yml)
                return config_yml
        else:
            self.log.error('ConfLoader.get_config: validate_yml failed')
            return config_yml
