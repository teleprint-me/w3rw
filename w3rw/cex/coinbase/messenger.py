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
from w3rw import __timeout__
from w3rw import __offset__
from w3rw import Response

from w3rw.cex.coinbase.abstract import AbstractAPI
from w3rw.cex.coinbase.abstract import AbstractAuth
from w3rw.cex.coinbase.abstract import AbstractMessenger

from requests.auth import AuthBase
from requests.models import PreparedRequest

import dataclasses
import hmac
import hashlib
import requests
import time


@dataclasses.dataclass
class API(AbstractAPI):
    __version: int = 2
    __url: str = 'https://api.coinbase.com'

    @property
    def version(self) -> int:
        return self.__version

    @property
    def url(self) -> str:
        return self.__url

    def endpoint(self, value: str) -> str:
        if value.startswith(f'/v{self.version}'):
            return value
        return f'/v{self.version}/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Auth(AbstractAuth, AuthBase):
    def __init__(self, key: str, secret: str):
        self.__key = key
        self.__secret = secret

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = str(int(time.time()))
        body = '' if request.body is None else request.body.decode('utf-8')
        message = f'{timestamp}{request.method.upper()}{request.path_url}{body}'
        headers = self.headers(timestamp, message)
        request.headers.update(headers)
        return request

    def signature(self, message: str) -> str:
        key = self.__secret.encode('ascii')
        msg = message.encode('ascii')
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def headers(self, timestamp: str, message: str) -> dict:
        return {
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'CB-ACCESS-KEY': self.__key,
            'CB-ACCESS-SIGN': self.signature(message),
            'CB-ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }


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
        return self.session.get(
            self.api.path(endpoint),
            params=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def post(self, endpoint: str, data: dict = None) -> Response:
        time.sleep(__timeout__)
        return self.session.post(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def page(self, endpoint: str, data: dict = None) -> Response:
        responses = []
        if not data:
            data = {'limit': __offset__}
        while True:
            response = self.get(endpoint, data)
            if 200 != response.status_code:
                return [response]
            if not response.json():
                break
            responses.append(response)
            page = response.json()['pagination']
            if not page['next_uri']:
                break
            data['starting_after'] = page['next_starting_after']
        return responses

    def close(self):
        self.session.close()
