# Coinbase Pro and Exchange

## Overview

1. Abstract

    The Abstract Base Interface for the `coinbase_pro` module

2. Messenger

    The Authentication and `requests` Adapters for the `coinbase_pro` module

3. Client

    The Messenger Adapter for the `coinbase_pro` module

4. Socket

    The `websocket-client` Adapter for the `coinbase_pro` module


## Quickstart

The easiest method to get started with storing your credentials is to just use a config file.
I will be using the `configparser` library here to keep examples simple.
There are other methods that can be utilized and deciding on which approach depends on the context and application.

- Create the config file

```sh
touch settings.ini
```

- Modify the `settings.ini` file

```ini
[coinbase_pro]
key = my_api_key
secret = my_api_secret
passphrase = my_api_passphrase
```

- REST API

```python
from w3rw.cex.coinbase_pro.messenger import Auth
from w3rw.cex.coinbase_pro.messenger import Messenger
from w3rw.cex.coinbase_pro.client import Client

from configparser import ConfigParser


def get_api(section: str) -> dict:
    config = ConfigParser()
    config.read('settings.ini')
    api = {'key': config[section]['key'],
           'secret': config[section]['secret'],
           'passphrase': config[section]['passphrase']}
    return api

api = get_api('coinbase_pro')
client = Client(Messenger(Auth(api['key'], api['secret'], api['passphrase'])))
```

- WSS API

```python
from w3rw.coinbase_pro.socket import get_message
from w3rw.coinbase_pro.socket import Auth
from w3rw.coinbase_pro.socket import Stream

from pprint import pprint

def get_api(section: str) -> dict:
    config = ConfigParser()
    config.read('settings.ini')
    api = {'key': config[section]['key'],
           'secret': config[section]['secret'],
           'passphrase': config[section]['passphrase']}
    return api

api = get_api('coinbase_pro')
stream = Stream(Auth(api['key'], api['secret'], api['passphrase']))

message = get_message()
stream.connect()
stream.send(message)

print('[Note] ^C to end stream')
sleep(1)
while True:
    try:
        pprint(stream.receive())
        sleep(1)
    except (KeyboardInterrupt,):
        break
```

## TODO

- [ ] Abstract
- [ ] Messenger
- [ ] Client
- [ ] Socket
