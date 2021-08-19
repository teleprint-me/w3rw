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
from ledger.api.factory import __agent__
from ledger.api.factory import __source__
from ledger.api.factory import __version__

from ledger.api.factory import AbstractAuth

from requests.auth import AuthBase
from requests.models import PreparedRequest

import base64
import hmac
import hashlib
import time


class Auth(AbstractAuth, AuthBase):
    def __init__(self, key: str, secret: str, passphrase: str = None):
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
            'User-Agent': f'{__agent__}/{__version__} {__source__}',
            'CB-ACCESS-SIGN': self.signature(message),
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.__key,
            'CB-ACCESS-PASSPHRASE': self.__passphrase,
            'Content-Type': 'application/json'
        }
