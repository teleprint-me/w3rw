# Abstract Base Interface

## Introduction

The ABI follows a mixture of the Factory and Strategy Patterns and determines how the Core and Middleware are implemented. You should be able to implement the Core and Middleware, irrespective of the API, once you understand the ABI. If any changes are made to the ABI, then it would follow that these changes would affect the Core and Middleware as well.

- You should utilize the Core API if you want to use a single exchange in your application.
- You should utilize the Middleware API if you want to use multiple exchanges in your application.

_Note: This documentation is for educational purposes and is not intended to be utilized directly._

## Global Variables

- `__agent__` defines who the request is made by
- `__source__` defines the URI pointing to the public repository
- `__version__` defines the library version
- `__offset__` defines the number of entries to be retrieved per request
- `__limit__` defines the maximum number of entries to be received during a request
- `__timeout__` defines how long to wait until the request fails

_Note: `__offset__` and `__limit__` are Kraken specific_

## Global Types

- `List` is defined as type `list` and `list[dict]`
- `Dict` is defined as type `dict` and `List`
- `Response` is defined as type `requests.Response` and `list[requests.Response]`

_Note: All other data types utilized are built-in._

## Class Definitions

All REST API implementations are modeled by the ABI. This means that all interfaces are the same and expect the same inputs. If there is any differnce in either the input or output, then that difference is subject to the platforms implementation.

A simpler way to explain it is that Coinbase, Coinbase Pro, and Kraken all will return different results because they each have unique designs that determines I/O operations based on the specified platform.

We can then come to 2 basic conclusions.

- The first conclusion is that all I/O will differ if utilizing the Core API as the I/O is platform dependent.
- The second conclusion is that all I/O will be the same if utilizing the Middleware API as it expects the same input and gives back the same output.

### AbstractAuth

```python
AbstractAuth(key: str, secret: str)
```
- AbstractAuth defines the Auth object which is used for authenticating requests
- AbstractAuth is a callable object and its implementation is platform dependent

### AbstractAPI

```python
AbstractAPI()
```

- AbstractAPI defines a dataclass that represents information pertaining to the given REST API.

_Note: There is no need to utilize this class directly as it is implemented automatically by the `AbstractMessenger` class_

### AbstractMessenger

```python
AbstractMessenger(auth: AbstractAuth)
```

- AbstractMessenger defines the `requests` wrapper. 
- This object is returned by executing the method `AbstractClient.get_messenger(key: str, secret: str)`

_Note: This is the class you'll want to use if you're interested in implementing a single REST API._

### AbstractClient

```python
AbstractClient(messenger: AbstractMessenger)
```

- AbstractClient defines the Middleware API used for simplifying complicated REST API requests.
- This object is returned by executing the method `AbstractClient.get_client(key: str, secret: str)`

_Note: This is the class you'll want to use if you're interested in implementing multiple REST API's._

### AbstractFactory

```python
AbstractFactory()
```

- AbstractFactory defines the `AbstractMessenger` and `AbstractClient` that will be constructed and returned.
