### Notify minimal notifyer
Smal service to send notifications to multiple services like Slack DataDog

currently supported services is Slack, DataDog


# configure service
add a .notify.yml
```yaml
slack:
  orgs:
    - name: foo
      token: xoxp-foobar

datadog:
  orgs:
    - name: foo
      api_key: foo
      app_key: foo
```


# running api in wsgi container
```bash
$ gunicorn notify.app:api
```


# API
GET health `/health` response 200 body: `{"status": "OK"}`


POST message `/api/notify`
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
