import requests
import json

class SmartLicensePortal:

    class Urls:
        accounts = {'method': 'GET', 'url': '/smart-accounts-and-licensing/v2/accounts'}
        reportUsage = {'method': 'POST', 'url': '/smart-accounts-and-licensing/v2/devices/reportusage'}
        requestAuthCode = {'method': 'POST', 'url': '/smart-accounts-and-licensing/v2/devices/authrequest'}
        poll = {'method': 'POST', 'url': '/smart-accounts-and-licensing/v2/accounts/poll'}

    def __init__(self, client_id, client_secret, sa_domain, cco_username=None, cco_password=None):
        self.base_url = 'https://swapi.cisco.com//services/api'
        self.sa_domain = sa_domain

        url = "https://cloudsso.cisco.com/as/token.oauth2"
        payload = f'client_id={client_id}&' \
                  f'client_secret={client_secret}&'
        if cco_username:
            payload += f'grant_type=password' \
                       f'username={cco_username}&' \
                       f'password={cco_password}'
        else:
            payload += f'grant_type=client_credentials'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PF=SWgJBK5J3KvQXCEhvNVwbT'
        }
        response = requests.request("POST", url, headers=headers, data=payload).json()
        self.access_token = response['access_token']
        # self.refresh_token = response['refresh_token']

    def api_call(self, method='GET', url='/', headers=None, payload=''):

        if headers is None:
            headers = {'Accept': '*/*'}
        headers['Authorization'] = f'Bearer {self.access_token}'
        response = requests.request(method=method, url=f'{self.base_url}{url}', headers=headers, data=json.dumps(payload))

        return response
