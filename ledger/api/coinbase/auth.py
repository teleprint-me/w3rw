# Ledger - A web application to track cryptocurrency investments
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
from ledger.api.factory import __agent__
from ledger.api.factory import __source__
from ledger.api.factory import __version__
from ledger.api.factory import AbstractToken
from ledger.api.factory import AbstractAuth

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
        self.__passphrase = passphrase

    @property
    def key(self) -> str:
        return self.__key

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def passphrase(self) -> str:
        return self.__passphrase

    def as_dict(self) -> dict:
        return {
            'key': self.key,
            'secret': self.secret,
        }


def get_timestamp() -> str:
    return str(time.time())


def get_request_body(request: PreparedRequest) -> str:
    return '' if request.body is None else request.body.decode('utf-8')


def get_message(timestamp: str, request: PreparedRequest) -> str:
    body = get_request_body(request)
    return f'{timestamp}{request.method.upper()}{request.path_url}{body}'


def get_b64signature(message: str, token: Token) -> bytes:
    key = base64.b64decode(token.secret)
    msg = message.encode('ascii')
    sig = hmac.new(key, msg, hashlib.sha256)
    digest = sig.digest()
    b64signature = base64.b64encode(digest)
    return b64signature.decode('utf-8')


def get_headers(timestamp: str, b64signature: bytes, token: Token) -> dict:
    return {
        'User-Agent': f'{__agent__}/{__version__} {__source__}',
        'CB-ACCESS-KEY': token.key,
        'CB-ACCESS-SIGN': b64signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }


class Auth(AbstractAuth, AuthBase):
    def __init__(self, key, secret):
        self.__token = Token(key, secret)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = get_timestamp()
        message = get_message(timestamp, request)
        b64signature = get_b64signature(message, self.__token)
        headers = get_headers(timestamp, b64signature, self.__token)
        request.headers.update(headers)
        return request

    @property
    def token(self) -> Token:
        return self.__token
