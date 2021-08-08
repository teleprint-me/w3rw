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
from ledger.api.factory import AbstractQuery

import base64
import hashlib
import hmac
import urllib
import time


def get_timestamp() -> str:
    return str(int(1000 * time.time()))


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

    @property
    def data(self) -> dict:
        return {
            'key': self.key,
            'secret': self.secret
        }


class Proxy(object):
    def __init__(self, query: AbstractQuery, token: AbstractToken):
        self.__query = query
        self.__token = token
        self.__timestamp = get_timestamp()

    @property
    def query(self) -> AbstractQuery:
        return self.__query

    @property
    def token(self) -> AbstractToken:
        return self.__token

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def message(self) -> bytes:
        post = urllib.parse.urlencode(self.query.data)
        encoded = (str(self.query.data['nonce']) + post).encode()
        return self.query.endpoint.encode() + hashlib.sha256(encoded).digest()

    @property
    def b64signature(self) -> bytes:
        message = self.message
        secret = base64.b64decode(self.token.secret)
        signature = hmac.new(secret, message, hashlib.sha512)
        b64signature = base64.b64encode(signature.digest())
        return b64signature.decode()

    @property
    def headers(self) -> dict:
        return {
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'API-Key': self.token.key,
            'API-Sign': self.b64signature,
        }


class Auth(AbstractAuth):
    def __init__(self, key: str, secret: str, passphrase: str = None):
        self.__token = Token(key, secret, passphrase)

    def __call__(self, query: AbstractQuery) -> dict:
        return Proxy(query, self.token).headers

    @property
    def token(self) -> Token:
        return self.__token

    @property
    def nonce(self) -> str:
        return get_timestamp()
