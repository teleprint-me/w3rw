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
from w3rw import Response

from w3rw.cex.coinbase_pro.abstract import AbstractAPI
from w3rw.cex.coinbase_pro.abstract import AbstractAuth
from w3rw.cex.coinbase_pro.abstract import AbstractMessenger
from w3rw.cex.coinbase_pro.abstract import AbstractSubscriber

from requests.auth import AuthBase
from requests.models import PreparedRequest

import base64
import dataclasses
import hmac
import hashlib
import requests
import time


@dataclasses.dataclass
class API(AbstractAPI):
    # NOTE: https://github.com/teleprint-me/ledger-api/discussions/7
    __version: int = 1
    __url: str = 'https://api.pro.coinbase.com'

    @property
    def version(self) -> int:
        return self.__version

    @property
    def url(self) -> str:
        return self.__url

    def endpoint(self, value: str) -> str:
        return f'/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Auth(AbstractAuth, AuthBase):
    def __init__(self, key: str, secret: str, passphrase: str):
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = str(time.time())
        body = str() if not request.body else request.body.decode('utf-8')
        message = f'{timestamp}{request.method.upper()}{request.path_url}{body}'
        headers = self.headers(timestamp, message)
        request.headers.update(headers)
        return request

    def signature(self, message: str) -> bytes:
        key = base64.b64decode(self.__secret)
        msg = message.encode('ascii')
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode('utf-8')

    def headers(self, timestamp: str, message: str) -> dict:
        return {
            'Content-Type': 'application/json',
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.__key,
            'CB-ACCESS-SIGN': self.signature(message),
            'CB-ACCESS-PASSPHRASE': self.__passphrase
        }


class Messenger(AbstractMessenger):
    def __init__(self, auth: AbstractAuth = None):
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

    def put(self, endpoint: str, data: dict = None) -> Response:
        time.sleep(__timeout__)
        return self.session.put(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def delete(self, endpoint: str, data: dict = None) -> Response:
        time.sleep(__timeout__)
        return self.session.delete(
            self.api.path(endpoint),
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

    def page(self, endpoint: str, data: dict = None) -> Response:
        responses = []
        if not data:
            data = {}
        while True:
            response = self.get(endpoint, data)
            if 200 != response.status_code:
                return [response]
            if not response.json():
                break
            responses.append(response)
            if not response.headers.get('CB-AFTER'):
                break
            data['after'] = response.headers.get('CB-AFTER')
        return responses

    def close(self):
        self.session.close()


class Subscriber(AbstractSubscriber):
    def __init__(self, messenger: AbstractMessenger):
        self.__messenger = messenger

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def error(self, response: requests.Response) -> bool:
        return 200 != response.status_code
