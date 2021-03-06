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
import base64
import hashlib
import hmac
import json
import time
import websocket


def get_default_message() -> dict:
    return {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }


def get_message(value: dict = None) -> dict:
    if value is None:
        return get_default_message()
    return value


class Token(object):
    def __init__(self, key: str, secret: str, passphrase: str):
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase

    def __call__(self) -> dict:
        timestamp = str(time.time())
        message = f'{timestamp}GET/users/self/verify'
        return {
            'signature': self.signature(message),
            'key': self.__key,
            'passphrase': self.__passphrase,
            'timestamp': timestamp
        }

    def signature(self, message: str) -> bytes:
        key = base64.b64decode(self.__secret)
        msg = message.encode('ascii')
        sig = hmac.new(key, msg, hashlib.sha256)
        digest = sig.digest()
        b64signature = base64.b64encode(digest)
        return b64signature.decode('utf-8')


class Stream(object):
    def __init__(self, auth: Token = None, url: str = None, trace: bool = False):
        self.auth: Token = auth
        self.url: str = url if url else 'wss://ws-feed.pro.coinbase.com'
        self.trace: bool = trace
        self.timeout: int = 30
        self.socket: websocket.WebSocket = None

    @property
    def connected(self) -> bool:
        return False if self.socket is None else self.socket.connected

    def connect(self) -> bool:
        header = None if self.auth is None else self.auth()
        websocket.enableTrace(self.trace)
        self.socket = websocket.create_connection(url=self.url, header=header)
        return self.connected

    def send(self, message: dict) -> None:
        if self.connected:
            self.socket.send(json.dumps(message))

    def receive(self) -> dict:
        if self.connected:
            payload = self.socket.recv()
            if payload:
                return json.loads(payload)
        return dict()

    def ping(self) -> None:
        payload = 'keepalive'
        while self.connected:
            if self.trace:
                print(f'[Ping] {payload} [Timeout] {self.timeout}s')
            self.socket.ping(payload)
            time.sleep(self.timeout)

    def disconnect(self) -> None:
        if self.connected:
            self.socket.close()
