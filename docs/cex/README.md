# w3rw.cex

CEx - Acronym for Centralized Exchange

## Contents

- Abstract
    - Details the Abstract Base Interface utilized for the w3rw.cex module.

- Messenger
    - Details the API, Auth, Messenger, and Subscriber Interfaces found within each of the respective w3rw.cex modules.

- Socket
    - Details the websocket-client Adapter.

## Importing

### REST

- Coinbase
    - Details the Coinbase Client Adapter.
    - [Official Coinbase Documentation](https://developers.coinbase.com/api/v2?shell#)

```python
from w3rw.cex.coinbase.messenger import Auth
from w3rw.cex.coinbase.messenger import Messenger
```

- Coinbase Pro
- Coinbase Exchange
    - Details the Coinbase Pro Client Adapter.
    - [Official Coinbase Pro Documentation](https://docs.cloud.coinbase.com/exchange/docs)

```python
from w3rw.cex.coinbase_pro.messenger import Auth
from w3rw.cex.coinbase_pro.messenger import Messenger
from w3rw.cex.coinbase_pro.client import Client
```

- Kraken
    - Details the Kraken Client Adapter.
    - [Official Kraken Documentation](https://docs.kraken.com/rest/)

```python
from w3rw.cex.kraken.messenger import Auth
from w3rw.cex.kraken.messenger import Messenger
from w3rw.cex.kraken.client import Client
```

### WebSocket

- Coinbase Pro

```python
from w3rw.cex.coinbase_pro.socket import Auth
from w3rw.cex.coinbase_pro.socket import Stream
```

- Kraken

```python
from w3rw.cex.kraken.socket import Auth
from w3rw.cex.kraken.socket import Stream
```
