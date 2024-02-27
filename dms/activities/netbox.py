from urllib.parse import urljoin
import requests


class NetboxHttp:

    def __init__(self, hostname, access_token):
        self.base_url = f'http://{hostname}'
        self.headers = {
            'Authorization': f'Token {access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def run(self, method: str, path: str, **kwargs):
        url = urljoin(self.base_url, f'api/{path}/')
        
        if method == 'get':
            r = requests.get(url, headers=self.headers, params=kwargs)
        elif method == 'post':
            r = requests.post(url, headers=self.headers, json=kwargs)
        elif method == 'patch':
            r = requests.patch(url, headers=self.headers)
        elif method == 'delete':
            r = requests.delete(url, headers=self.headers)
        else:
            return None

        r.raise_for_status()

        return r.json()
