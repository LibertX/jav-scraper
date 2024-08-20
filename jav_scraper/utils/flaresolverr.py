import os
import requests

from .singleton import Singleton

class Flaresolverr(metaclass = Singleton):
    _flaresolverr_url: str
    _flaresolverr_session: str

    def __init__(self):
        self._flaresolverr_url = os.environ.get('FLARESOLVERR_URL')
        if not self._flaresolverr_url:
            self._flaresolverr_url = 'http://localhost:8191'
        self._flaresolverr_url += '/v1'
        self.create_session()

    def create_session(self):
        headers = { "Content-Type": "application/json" }
        data = {
            "cmd": "sessions.create",
            "url": "https://www.google.com/",
            "session": 'jav-scraper',
            "maxTimeout": 60000
        }
        response = requests.post(self._flaresolverr_url, headers=headers, json=data)
        if response.json()['status'] != 'ok':
            raise Exception('Flaresolverr error')

        self._flaresolverr_session = response.json()['session']

    def read_url(self, url):
        headers = {"Content-Type": "application/json"}
        data = {
            "cmd": "request.get",
            "maxTimeout": 10000,
            "session": self._flaresolverr_session,
            "url": url
        }
        response = requests.post(self._flaresolverr_url, headers=headers, json=data)

        if response.json()['status'] != "ok":
            return False

        return response.json()

    def read_url_and_retry(self, url):
        response = self.read_url(url)
        if response:
            return response['solution']['response']
        else:
            self.destroy_session()
            self.create_session()
            response = self.read_url(url)
            if response:
                return response['solution']['response']
            else:
                return False

    def destroy_session(self):
        headers = { "Content-Type": "application/json" }
        data = {
            "cmd": "sessions.destroy",
            "session": self._flaresolverr_session
        }
        response = requests.post(self._flaresolverr_url, headers=headers, json=data)
        return response.json()['status'] == 'ok'
