import certifi
import collections
import hashlib
import hmac
import json
import time
import urllib3

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def lookup_function(**kwargs):
    field_name = kwargs.get('field_name')
    password_id = kwargs.get('password_id')
    private_key = kwargs.get('private_key')
    public_key = kwargs.get('public_key')
    url = kwargs.get('url')
    request_uri = 'api/v4/passwords/{0}.json'.format(password_id)

    timestamp = int(time.time())
    unhashed = f'{request_uri}{timestamp}'

    message_hash = hmac.new(
        key=private_key.encode('utf-8'),
        msg=unhashed.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest().lower()

    headers = {
        'X-Public-Key': public_key,
        'X-Request-Hash': message_hash,
        'X-Request-Timestamp': str(timestamp),
        'Content-Type': 'application/json; charset=utf-8'
    }

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    resp = http.request('GET', f'{url}{request_uri}', headers=headers)
    if resp.status != 200:
        raise PermissionError('Do not have permissions to access the requested password: [{0}].'.format(password_id))
    else:
        data = json.loads(resp.data.decode('utf-8'))
        if field_name not in data:
            raise ValueError('Field name [{0}] was not found in password: [{1}]'.format(field_name, password_id))
        return data[field_name]

tpm_plugin = CredentialPlugin(
    'Team Password Manager',
    inputs={
        'fields': [
            {
                'id': 'url',
                'label': 'Server URL',
                'type': 'string'
            },
            {
                'id': 'private_key',
                'label': 'Private Key',
                'type': 'string',
                'secret': True
            },
            {
                'id': 'public_key',
                'label': 'Public Key',
                'type': 'string'
            }
        ],
        'metadata': [
            {
                'id': 'password_id',
                'label': 'Password Id',
                'type': 'string',
                'help_text': 'The Id of the password record.'
            },
            {
                'id': 'field_name',
                'label': 'Field Name',
                'type': 'string',
                'help_text': 'Field in Team Password Manager to extract.'
            }
        ],
        'required': ['url', 'private_key', 'public_key', 'password_id', 'field_name'],
    },
    backend = lookup_function
)
