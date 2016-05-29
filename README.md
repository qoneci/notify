### Notify minimal notifyer
Smal service to send notifications to multiple services like Slack Hipchat DataDog

currently supported services is Slack, HipChat, DataDog


# configure service
add a .notify.yml
'''yaml
slack:
  orgs:
    - name: foo
      token: xoxp-foobar

hipchat:
  orgs:
    - name: foo
      token: bar

datadog:
  orgs:
    - name: foo
      token: bar
'''


# running api in wsgi container
'''bash
$ gunicorn notify.app:api
'''


# API
GET health
`/health`
respose `{"status": "OK"}`


POST message
`/api/notify`

body: application/json
```bash 
{
    "org_name": string,
    "channel_name": string,
    "message": string,
    "services": list,
}
```

response: 201
