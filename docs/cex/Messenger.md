# Messenger

The Messenger module defines the API, Auth, Messenger, and Subscriber classes. In most cases, you will only need to instantiate the Auth and Messenger classes. The Subscriber classes are used to define the Client interfaces. The Subscriber class can also be used to inherit from the Messenger class to define an extension or plugin for the Clients implentation.

## API

```python
API(version: int = None, url: str = None)
```

The API class defines the REST API URI path utilized by Messenger.

_Note: There is no need to utilize this class as it is instantiated and handled by the Messenger class._

### API.verison

```python
API.version -> int
```

A read-only property and returns the REST API Version number.

### API.url

```python
API.url -> str
API.url: str = 'https://api.domain.com'
```

A read-write property and returns the REST API domain being used.

### API.endpoint

```python
API.endpoint(value: str) -> str
```

A method that returns the URI path to be used.

### API.path

```python
API.path(value: str) -> str
```

A method that returns the full URI path to be used.

## Auth

```python
# Coinbase and Kraken
Auth(key: str, secret: str)
# Coinbase Pro and Coinbase Exchange
Auth(key: str, secret: str, passphrase: str)
```

The Auth class defines the REST API Authentication method utilized by Messenger.

_Note: There is no need to utilize this class as it is instantiated and handled by the Messenger class._

### Auth.__call__

Auth is a callable object and what it returns is platform dependent.

```python
# Coinbase, Coinbase Pro, and Coinbase Exchange
Auth.__call__(request: PreparedRequest) -> PreparedRequest
# Kraken
Auth.__call__(endpoint: str, data: dict) -> dict
```

The callable instance `auth()` returns the authentication headers for the target REST API.

### Auth.nonce

```python
# Kraken
Auth.nonce -> str
```

A Kraken specific implementation and is a read-only property that returns the timestamp used to sign the headers for the given request.

### Auth.signature

```python
# Coinbase, Coinbase Pro, and Coinbase Exchange
Auth.signature(message: str) -> bytes
# Kraken
Auth.signature(endpoint: str, data: dict) -> bytes
```

A method that returns a signed message.

### Auth.headers

```python
# Coinbase, Coinbase Pro, and Coinbase Exchange
Auth.headers(timestamp: str, message: str) -> dict
```

A Coinbase* specific implementation and that returns the signed headers which are injected into the given request.

_Note: Coinbase* refers to Coinbase, Pro, and Exchange._

## Messenger

```python
Messenger(auth: AbstractAuth)
```

The Messenger class defines the requests adapter utilized to facilitate communication with the REST API.

_Note: Coinbase Exchange clients will want to modify the Messenger.api.url property to point to the desired domain which is https://api.exchange.coinbase.com_

_Warning: Do not abuse the REST API calls by polling requests. If you need to poll a request, then you should utilize the `websockets-client` instead. I will be supporting a `sockets` module for Coinbase Pro, Coinbase Exchange, and Kraken._

### Messenger.auth

```python
Messenger.auth -> AbstractAuth
```

A read-only property that returns the Auth instance object being used to authenticate requests.

### Messenger.api

```python
Messenger.api -> AbstractAPI
```

A read-only property that returns the API instance object being used to create requests.

### Messenger.timeout

```python
Messenger.timeout -> int
```

A read-only property that returns the number of seconds to wait before timing out a given request.

### Messenger.session

```python
Messenger.session -> Session
```

A read-only property that returns the Session instance object being used to create requests.

### Messenger.get

```python
Messenger.get(endpoint: str, data: dict = None) -> Response
```

A method that returns a Response instance object created by `session.get()`.

### Messenger.post

```python
Messenger.post(endpoint: str, data: dict = None) -> Response
```

A method that returns a Response instance object created by `session.post()`.

### Messenger.put

```python
# Coinbase Pro and Coinbase Exchange only
Messenger.put(endpoint: str, data: dict = None) -> Response
```

A Coinbase Pro and Coinbase Exchange specific method that returns a Response instance object created by `session.put()`.

### Messenger.delete

```python
# Coinbase Pro and Coinbase Exchange only
Messenger.delete(endpoint: str, data: dict = None) -> Response
```

A Coinbase Pro and Coinbase Exchange specific method that returns a Response instance object created by `session.delete()`.

### Messenger.page

```python
Messenger.page(endpoint: str, data: dict = None) -> Response
```

A method that returns a Response instance object created by `session.get()` or `session.post`.

_Note: This method will always return a `list` of Response objects._

### Messenger.close

```python
Messenger.close() -> None
```

A method that calls the `Session.close()` method.

## Subscriber

```python
Subscriber(messenger: AbstractMessenger)
```

The Subscriber is utilized by inheriting classes that define scoped methods utilized by the Client class.

### Subscriber.messenger

```python
Subscriber.messenger -> AbstractMessenger
```

A read-only property that returns the given Messenger instance object.

### Subscriber.error

```python
Subscriber.error(response: Response) -> bool
```

A method that returns a true if the response status code is not 200, otherwise it returns False.
