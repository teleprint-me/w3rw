# Overview

The library is broken down by type and interface.

```sh
$ tree -d w3rw
w3rw
├── cex
│   ├── coinbase
│   ├── coinbase_pro
│   └── kraken
├── dex
└── wallet

6 directories
```

- An example of type would be a Centralized Exchange, or CEx for short.
- An example of interface would be Coinbase Pro.

Just import based on the exchange you're interested in implementing.

```python
from w3rw.cex.coinbase.messenger import Auth
from w3rw.cex.coinbase.messenger import Messenger
messenger = Messenger(Auth(key, secret)
```

You can find more information in the docs which is sectioned by module.

```sh
$ tree -d docs
docs
├── coinbase
├── coinbase_pro
└── kraken

3 directories
```

## Notes

### Docs
- Will be implemented on a per module basis.
- Will only be available for currently existing code.

### Coinbase Exchange
- Clients will want to use the `coinbase_pro` module. 
- Pro and Exchange are nearly identical interfaces and only require you to modify the API URL. 
- More information can be found in the docs.
