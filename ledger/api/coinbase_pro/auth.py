# Ledger-API - Core REST API for teleprint-me/ledger
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
from api.factory import __agent__
from api.factory import __source__
from api.factory import __version__
from api.factory import AbstractToken
from api.factory import AbstractAuth

from requests.auth import AuthBase
from requests.models import PreparedRequest

import base64
import hmac
import hashlib
import time


class Token(AbstractToken):
    def __init__(self, key: str, secret: str, passphrase: str = None):
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase if passphrase else ''

    @property
    def key(self) -> str:
        return self.__key

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def passphrase(self) -> str:
        return self.__passphrase

    @property
    def data(self) -> dict:
        return {
            'key': self.key,
            'secret': self.secret,
            'passphrase': self.passphrase
        }


class Proxy(object):
    def __init__(self, token: Token, request: PreparedRequest):
        self.__token = token
        self.__request = request
        self.__timestamp = str(time.time())

    @property
    def token(self) -> Token:
        return self.__token

    @property
    def request(self) -> PreparedRequest:
        return self.__request

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def body(self) -> str:
        if not self.request.body:
            return ''
        return self.request.body.decode('utf-8')

    @property
    def message(self) -> str:
        return f'{self.timestamp}' \
               f'{self.request.method}' \
               f'{self.request.path_url}' \
               f'{self.body}'

    @property
    def b64signature(self) -> bytes:
        key = base64.b64decode(self.token.secret)
        message = self.message.encode('ascii')
        signature = hmac.new(key, message, hashlib.sha256)
        b64signature = base64.b64encode(signature.digest())
        return b64signature.decode('utf-8')

    @property
    def headers(self) -> dict:
        return {
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'CB-ACCESS-SIGN': self.b64signature,
            'CB-ACCESS-TIMESTAMP': self.timestamp,
            'CB-ACCESS-KEY': self.token.key,
            'CB-ACCESS-PASSPHRASE': self.token.passphrase,
            'Content-Type': 'application/json'
        }


class Auth(AbstractAuth, AuthBase):
    def __init__(self, key: str, secret: str, passphrase: str = None):
        self.__token = Token(key, secret, passphrase)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        proxy = Proxy(self.token, request)
        request.headers.update(proxy.headers)
        return request

    @property
    def token(self) -> Token:
        return self.__token
