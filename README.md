# ledger-api

```
 _       _                 _       _
| |_ ___| | ___ _ __  _ __(_)_ __ | |_   _ __ ___   ___ 
| __/ _ \ |/ _ \ '_ \| '__| | '_ \| __| | '_ ` _ \ / _ \
| ||  __/ |  __/ |_) | |  | | | | | |_ _| | | | | |  __/
 \__\___|_|\___| .__/|_|  |_|_| |_|\__(_)_| |_| |_|\___|
               |_|
 _          _                                  _ 
| | ___  __| | __ _  ___ _ __       __ _ _ __ (_)
| |/ _ \/ _` |/ _` |/ _ \ '__|____ / _` | '_ \| |
| |  __/ (_| | (_| |  __/ | |_____| (_| | |_) | |
|_|\___|\__,_|\__, |\___|_|        \__,_| .__/|_|
              |___/                     |_|
```

## About

A `requests` wrapper for interfacing with Centralized and Decentralized Cryptocurrency REST API's.

## Notes

- This library is a dependency of the [teleprint-me/ledger](https://github.com/teleprint-me/ledger) repository.
- This library is intentionally minimalist and targets only REST API's.
- This library is a work in progress and is subject to change. 
- There may be aspects of this library that are broken, buggy, or missing from the implementation.
- There is NO WARRANTY, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.

## Install

```sh
git clone https://github.com/teleprint-me/ledger-api.git
cd ledger-api
virtualenv venv
source venv/bin/activate
pip install -r requirements 
```

_Note: Packaging support for `pip` will be added at some point in the future._

## Docs

There are 3 parts to this API.

- [ABI Documentation](https://github.com/teleprint-me/ledger-api/tree/main/docs)

    The ABI consists of the general design of the overall project. This design defines the general interface for all REST API's within this repository.

- [Core Documentation](https://github.com/teleprint-me/ledger-api/blob/main/docs/Core.md)

    The Core is the implementation of the ABI which is used to communicate with the intended REST API.

- [Middleware Documentation](https://github.com/teleprint-me/ledger-api/blob/main/docs/Middleware.md)

    The middleware builds on the Core and consists of a modified REST API for simplifying complicated requests through the use of the Factory Pattern.

## Tips

- Bitcoin (Segwit): 3E1YSahzUnYYx2RTuRt4KWogDBCsdCS1n3
- Ethereum: 0x7be933221135468b9886632771fF289341144C3a
- Litecoin (Segwit): MMNDfhgc3jfs3XJoJ7DSCedBp742dH12jD

## TODO

### Documentation

- [ ] ABI
- [ ] Core
- [ ] Middleware

### Package Management

- [ ] ???

### Centralized Exchanges

- [ ] Coinbase
- [x] Coinbase Pro
- [x] Kraken
- [ ] Gemini

### Dencentralized Exchanges

- [ ] 1inch
- [ ] Uniswap
- [ ] Compound

### Wallets

- [ ] Coinbase Wallet
- [ ] Metamask Wallet
- [ ] Ledger Wallet

### Tests

- [ ] Coinbase
- [ ] Coinbase Pro
- [ ] Kraken
- [ ] Gemini
- [ ] 1inch
- [ ] Uniswap
- [ ] Compound
- [ ] Coinbase Wallet
- [ ] Metamask Wallet
- [ ] Ledger Wallet

#### A Note on Testing

There is no method to gaurentee testing. Only a guarentee to verify code integrity. Testing these API's is difficult seeing as some do not support a sandbox for testing. The major pitfall to this is that exploratory testing is required to verify that the code is functioning as intended. This makes bugs difficult to pinpoint. If testing is implemented at any point in time, then it should be implemented to verify the structure of the code instead.
