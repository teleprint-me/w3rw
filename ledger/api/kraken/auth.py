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
from ledger.api.factory import AbstractAuth

import base64
import hashlib
import hmac
import urllib
import time


class Auth(AbstractAuth):
    def __init__(self, key: str, secret: str):
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
