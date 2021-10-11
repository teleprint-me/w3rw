from w3rw.cex.kraken.messenger import Auth
from w3rw.cex.kraken.messenger import Messenger

import json
import websocket
import time


# Array of currency pairs.
# Format of each pair is "A/B",
# where A and B are ISO 4217-A3 for standardized assets
# and popular unique symbol if not standardized.
def get_default_message() -> dict:
    return {
        'event': 'subscribe',
        'pair': ['XBT/USD'],
        'subscription': {
            'name': 'ticker'
        }
    }


def get_message(value: dict = None) -> dict:
    if value is None:
        value = get_default_message()
    return value


class Token(object):
    def __init__(self, key: str, secret: str):
        self.__messenger = Messenger(Auth(key, secret))

    def __call__(self) -> str:
        self.__response = self.messenger.post('/private/GetWebSocketsToken')
        if self.error:
            raise ValueError('Failed to get authentication token from kraken')
        return self.__response['result']['token']

    @property
    def response(self) -> dict:
        return self.__response

    @property
    def error(self) -> list:
        return self.__response['error']

    @property
    def expires(self) -> int:
        if self.error:
            raise ValueError('Failed to get authentication token from kraken')
        return self.__response['result']['expires']


class Stream(object):
    def __init__(self, auth: Token = None, url: str = None, trace: bool = False):
        self.auth: Token = auth
        self.url: str = url if url else 'wss://ws.kraken.com'
        self.trace: bool = trace
        self.timeout: int = 30
        self.socket: websocket.WebSocket = None

    @property
    def connected(self) -> bool:
        return False if self.socket is None else self.socket.connected

    def connect(self) -> bool:
        websocket.enableTrace(self.trace)
        self.socket = websocket.create_connection(self.url)
        return self.connected

    def send(self, params: dict) -> bool:
        if self.connected:
            if self.auth and 'subscription' in params:
                params['subscription'].update({'token': self.auth()})
            payload = json.dumps(params)
            self.socket.send(payload)
            return True
        return False

    def receive(self) -> dict:
        if self.connected:
            payload = self.socket.recv()
            return json.loads(payload)
        return dict()

    def ping(self) -> None:
        payload = 'keepalive'
        while self.connected:
            if self.trace:
                print(f'[Ping] {payload} [Timeout] {self.timeout}s')
            self.socket.ping(payload)
            time.sleep(self.timeout)

    def disconnect(self) -> bool:
        if self.connected:
            self.socket.close()
            return True
        return False
