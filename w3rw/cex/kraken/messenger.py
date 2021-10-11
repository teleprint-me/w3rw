# w3rw - A Wrapper for Cryptocurrency Interfaces
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from w3rw import __agent__
from w3rw import __source__
from w3rw import __version__
from w3rw import __offset__
from w3rw import __limit__
from w3rw import __timeout__
from w3rw import Response

from w3rw.cex.abstract import AbstractAPI
from w3rw.cex.abstract import AbstractAuth
from w3rw.cex.abstract import AbstractMessenger
from w3rw.cex.abstract import AbstractSubscriber

import base64
import dataclasses
import hashlib
import hmac
import requests
import time
import urllib


@dataclasses.dataclass
class API(AbstractAPI):
    __version: int = 0
    __url: str = 'https://api.kraken.com'

    @property
    def version(self) -> int:
        return self.__version

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value

    def endpoint(self, value: str) -> str:
        if value.startswith(f'/{self.version}'):
            return value
        return f'/{self.version}/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Auth(AbstractAuth):
    def __init__(self, key: str = None, secret: str = None):
        self.__key = key
        self.__secret = secret

    def __call__(self, endpoint: str, data: dict) -> dict:
        return {
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'API-Key': self.__key,
            'API-Sign': self.signature(endpoint, data)
        }

    @property
    def nonce(self) -> str:
        return str(int(1000 * time.time()))

    def signature(self, endpoint: str, data: dict) -> bytes:
        key = base64.b64decode(self.__secret)
        post = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + post).encode()
        message = endpoint.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(key, message, hashlib.sha512)
        signature = base64.b64encode(mac.digest())
        return signature.decode()


class Messenger(AbstractMessenger):
    def __init__(self, auth: AbstractAuth):
        self.__auth: AbstractAuth = auth
        self.__api: AbstractAPI = API()
        self.__session: requests.Session = requests.Session()
        self.__timeout: int = 30

    @property
    def auth(self) -> AbstractAuth:
        return self.__auth

    @property
    def api(self) -> AbstractAPI:
        return self.__api

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def session(self) -> requests.Session:
        return self.__session

    def get(self, endpoint: str, data: dict = None) -> Response:
        time.sleep(__timeout__)
        endpoint = self.api.endpoint(endpoint)
        if not data:
            data = {}
        data['nonce'] = self.auth.nonce
        return self.session.get(
            self.api.path(endpoint),
            params=data,
            headers=self.auth(endpoint, data),
            timeout=self.timeout
        )

    def post(self, endpoint: str, data: dict = None) -> Response:
        time.sleep(__timeout__)
        endpoint = self.api.endpoint(endpoint)
        if not data:
            data = {}
        data['nonce'] = self.auth.nonce
        return self.session.post(
            self.api.path(endpoint),
            data=data,
            headers=self.auth(endpoint, data),
            timeout=self.timeout
        )

    def page(self, endpoint: str, data: dict = None) -> Response:
        responses = []
        if not data:
            data = {}
        data['ofs'] = 0
        while data['ofs'] < __limit__:
            response = self.post(endpoint, data)
            ok = 200 == response.status_code
            error = response.json().get('error')
            if not ok or error:
                return [response]
            if not response.json().get('result'):
                break
            responses.append(response)
            data['ofs'] += __offset__
        return responses

    def close(self) -> None:
        self.session.close()


class Subscriber(AbstractSubscriber):
    def __init__(self, messenger: AbstractMessenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def error(self, response: requests.Response) -> bool:
        return not response.json()['error']
