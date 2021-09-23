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
from w3rw import __agent__
from w3rw import __source__
from w3rw import __version__

from w3rw.factory import AbstractAuth

from requests.auth import AuthBase
from requests.models import PreparedRequest

import hmac
import hashlib
import time


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
