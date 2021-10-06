# Overview

The library is broken down by TYPE, INTERFACE, and MODULE. From there, we can import a CLASS or FUNCTION definition depending on what platform we're interested in.

```sh
$ tree w3rw
w3rw
├── cex
│   ├── coinbase
│   │   ├── abstract.py
│   │   ├── __init__.py
│   │   └── messenger.py
│   ├── coinbase_pro
│   │   ├── abstract.py
│   │   ├── client.py
│   │   ├── __init__.py
│   │   ├── messenger.py
│   │   └── socket.py
│   ├── __init__.py
│   └── kraken
│       ├── abstract.py
│       ├── __init__.py
│       ├── messenger.py
│       └── socket.py
├── dex
│   └── __init__.py
├── __init__.py
└── wallet
    └── __init__.py

6 directories, 16 files
```

An example of

- TYPE would be `cex`.
- INTERFACE would be `coinbase_pro`.
- MODULE would be `messenger`.
- CLASS or FUNCTION would be `Messenger`

### Example

```python
from w3rw.TYPE.INTERFACE.MODULE import CLASS
```

### Example 

```python
from w3rw.cex.kraken.messenger import Auth
from w3rw.cex.kraken.messenger import Messenger
```

You can find more information in the docs which is sectioned by TYPE.

```sh
$ tree docs
docs
├── cex
│   ├── Abstract.md
│   ├── CoinbasePro.md
│   ├── Kraken.md
│   ├── Messenger.md
│   └── Socket.md
├── INSTALL.md
└── README.md

1 directory, 7 files
```

## Globals

The `w3rw` library has a few abstract types and global variables which are utilized by the API implementations as well as the python `setuptools` package. These variables are defined in the `w3rw.__init__` module.

### Variables

- `__agent__` defines who the request is made by
- `__source__` defines the URI pointing to the public repository
- `__version__` defines the library version
- `__offset__` defines the number of entries to be retrieved per request
- `__limit__` defines the maximum number of entries to be received during a request
- `__timeout__` defines how long to wait before the request fails

_Note: `__offset__` and `__limit__` are Coinbase and Kraken specific_

### Types

- `List` is defined as type `list` and `list[dict]`
- `Dict` is defined as type `dict` and `List`
- `Response` is defined as type `requests.Response` and `list[requests.Response]`

_Note: All other data types utilized are built-in._

## Notes

- This library is intentionally minimalist.

### Docs

- Are implemented on a per module basis.
- Are only be available for currently existing code.
- It helps if you familiarize your self with the Official Docs of your target API.

### Issues

- If you find a bug or error, then you should open an issue and report as much information as is relavent to issue you're experiencing. 
- Remember to omit your API Key information. 
- It's good practice to store your API Key externally from your environment.

### Contributions

- Anyone can help with the Documentation or Code Base.
    - GPG Signatures are required to make Pull Requests.
- Leave a Tip if you would like to support this project financially.
    - I put a lot of time, effort, and energy into creating and maintaining this project. 
    - Every Sat, Gwei, or Litoshi goes a long way!

### Coinbase Exchange

- Clients will want to use the `coinbase_pro` module. 
- Pro and Exchange are nearly identical interfaces and only require you to modify the API URL. 
- More information can be found in the docs.
