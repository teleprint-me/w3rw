# Core Interface

## Introduction

The Core Interface is the implementation of the ABI. All REST API Interfaces follow the same strategy when implemented. This allows for flexibility in the Middleware Implementation which ties it all together.

- You should utilize the Core API if you want to use a single exchange in your application.
- You should utilize the Middleware API if you want to use multiple exchanges in your application.

## Class Definitions

### Auth

```python
# Most API's utilize a Key and Secret pair for client authentication.
Auth(key: str, secret: str)
# Coinbase Pro consumers will be required to add a passphrase argument.
Auth(key: str, secret: str, passphrase: str)
```

- Auth object is used for authenticating requests

_Note: This object is passed to the Messenger class as an argument during instantiation. More information can be found below._

```python
from w3rw.kraken.auth import Auth

key = 'My API Key'
secret = 'My API Secret'

auth = Auth(key, secret)
```

### Messenger

```python
Messenger(auth: AbstractAuth)
```

- Messenger implements the `requests` wrapper. 
- This object is returned by executing the method `AbstractFactory.get_messenger(key: str, secret: str)`

_Note: This is the class you'll want to use if you're interested in implementing a single REST API._

```python
from w3rw.kraken.auth import Auth
from w3rw.kraken.messenger import Messenger

key = 'My API Key'
secret = 'My API Secret'

# Instantiate the Messenger object
messenger = Messenger(Auth(key, secret))
```

#### Messenger Properties

Messenger has 4 read-only properties.

```python
# These should be self explantory.
messenger.api -> AbstractAPI
messenger.auth -> AbstractAuth
messenger.session -> requests.Session
messenger.timeout -> int
```

#### Messenger Methods

Messenger has 4 methods.

```python
# Make a GET request
messenger.get(endpoint: str, data: dict = None) -> Response
# Make a POST request
messenger.post(endpoint: str, data: dict = None) -> Response
# Paginate a GET request
messenger.page(endpoint: str, data: dict = None) -> Response
# End the requests session
messenger.close()
```

### Example

```python
from w3rw.coinbase_pro.client import CoinbaseProFactory

key = 'My API Key'
secret = 'My API Secret'
passphrase = 'My API Passphrase'

factory = CoinbaseProFactory()
cbpro = factory.get_messenger(key, secret, passphrase)
response = cbpro.get('/accounts')

if 200 == response.status_code:
    print(response.json()[0])
else:
    print('[Error]', response.json()['message'])
```
