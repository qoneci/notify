### Notify minimal notifyer
Smal service to send notifications to multiple services like Slack DataDog.
currently supported services is Slack, DataDog

written to work in python3.5


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
    "message": string,
    "services": list,
    "channel_name": string,
    "tags": list,               # optional needed for datadog
    "alert_type": string        # optional needed for datadog
}
```

response: 201

# install
```bash
$ virtualenv venv
$ source venv/bin/activate
pip3 install -r requirements.txt

```


# example use 
first start the server and configure the intergration you like to use. The follwing example will
send two events one to slack and one to datadog. for slack it will send it to the `qoneci` org
with the messame `foo bar` in channel `test`. For datadog it will send a event with title `info`
message `foo bar` and alert level `info` and tags `testing:test`
```bash
$ gunicorn notify.app:api
```

```python
import json
import requests
body = {
    'org_name': 'qoneci',
    'message': 'foo bar',
    'services': ['slack', 'datadog'],
    'channel_name': 'test',
    'alert_type': 'info',
    'tags': ['testing:test'],
}
url = 'http://127.0.0.1:8000/api/notify'
headers = {'content-type': 'application/json'}

In [9]: requests.post(url, headers=headers, data=json.dumps(body))
Out[9]: <Response [201]>

```
