from slackclient import SlackClient
from notify.core import config_parser


class Slack(object):
    def __init__(self, org_name):
        self.org_name = org_name
        self.slack_conf = {}
        self.conf = {}
        self.slack_client = None

    def _get_client(self):
        return self.slack_client

    def _get_conf(self):
        return self.conf

    def _get_slack_conf(self):
        return self.slack_conf

    def init_client(self):
        self.conf = config_parser.ConfLoader().get_config('slack')
        if self.conf:
            self.slack_conf = config_parser.Config(self.conf).get_service('slack', self.org_name)

        if self.slack_conf:
            self.slack_client = SlackClient(self.slack_conf[0].get('token'))

    def _call(self, command):
        return self.slack_client.api_call(command)

    def _auth_test(self):
        return self._call('auth.test')

    def _api_test(self):
        return self._call('api.test')

    def channels_list(self):
        channels = self._call('channels.list')
        if channels.get('ok'):
            return channels
        else:
            return {}

    def channels_names_and_id(self):
        result = {}
        ch = self.channels_list()
        if ch:
            return {x.get('name'): x.get('id') for x in ch['channels']}
        else:
            return result

    def send_message(self, channel_id, message):
        sent = self.slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username='notify bot',
            icon_emoji=':see_no_evil:'
        )
        return sent


class HipChat(object):
    def __init__(self):
        pass


class DataDog(object):
    def __init__(self):
        pass
