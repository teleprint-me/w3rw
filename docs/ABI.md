# Abstract Base Interface

## Introduction

The ABI follows a mixture of patterns and determines how the Core and Middleware are implemented. You should be able to implement the Core and Middleware, irrespective of the API, once you understand the ABI. If any changes are made to the ABI, then it would follow that these changes would affect the Core and Middleware as well.

- You should utilize the Core API if you want to use a single exchange in your application.
- You should utilize the Middleware API if you want to use multiple exchanges in your application.

_Note: This documentation is for educational purposes and is not intended to be utilized directly._

## Global Variables

- `__agent__` defines who the request is made by
- `__source__` defines the public repository URL
- `__version__` defines the library version
- `__timeout__` defines rate limiting value
- `__offset__` defines the number of entries to be retrieved per request
- `__limit__` defines the maximum number of entries to be received during a request

_Note: `__offset__` and `__limit__` are Kraken specific_

## Global Types

- `List` is defined as type `list` and `list[dict]`
- `Dict` is defined as type `dict` and `List`
- `Response` is defined as type `requests.Response` and `list[requests.Response]`

_Note: All other data types utilized are built-in._

## Class Definitions

Implementations are modeled by the ABI and interfaces are identical except where implementations differ. If there is any difference in either the input or output, then that difference is subject to the platforms implementation.

We can then come to 2 basic conclusions.

- The first conclusion is that all I/O will differ if utilizing the Core API as the I/O is platform dependent.
- The second conclusion is that all I/O will be the same if utilizing the Middleware API as it expects the same input and gives back the same output. Any variation that may occur during I/O is platform dependent.

### AbstractAuth

```python
AbstractAuth(key: str, secret: str)
```

The AbstractAuth definition is a Authentication Adapter. This definition is implementation specific and is not utilized directly. It is simply instantiated with authentication information and passed to the Messenger which then utilizes the Auth instance.

- AbstractAuth defines the Auth object which is used for authenticating requests
- AbstractAuth is a callable object and its implementation is platform dependent

### AbstractAPI

```python
AbstractAPI()
```

The AbstractAPI definition is a URL Adapter. This definition is implementation specific and is not utilized directly. There is no need to instantiate this class as it is instantiated automatically by the AbstractMessenger definition.

- AbstractAPI defines a dataclass that represents information pertaining to the given REST API.

### AbstractMessenger

```python
AbstractMessenger(auth: AbstractAuth)
```

The AbstractMessenger is a `requests` Adapter. It automates authentication requests by handling the naunces of making platform specific requests. It handles GET and POST requests and may paginate requests through the use of either a GET or POST request.

- AbstractMessenger defines the `requests` wrapper. 
- This object is returned by executing the method `AbstractFactory.get_messenger(key: str, secret: str)`

_Note: This is the class you'll want to use if you're interested in implementing a single REST API._

### AbstractClient

```python
AbstractClient(messenger: AbstractMessenger)
```

The AbstractClient is a Facade. It simplifies requests by unifying I/O except where I/O may be implementation specific. This makes it possible to manage multiple clients by utilizing identical I/O.

- AbstractClient defines the Middleware API used for simplifying complicated requests.
- This object is returned by executing the method `AbstractFactory.get_client(key: str, secret: str)`

_Note: This is the class you'll want to use if you're interested in implementing multiple REST API's._

### AbstractFactory

```python
AbstractFactory()
```

The AbstractFactory is a Builder/Factory. It simply instantiates either a AbstractMessenger or a AbstractClient.

- AbstractFactory defines the `AbstractMessenger` and `AbstractClient` objects that will be constructed and returned.