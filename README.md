# `ledger-api`

## About

A `requests` wrapper for interfacing with both centralized and decentralized REST based Application Programming Interfaces.

## Note

This library is a work in progress. There may be aspects of this library that are broken, buggy, or missing from the implementation.

## Install

```sh
git clone https://github.com/teleprint-me/ledger-api.git
cd ledger-api
virtualenv venv
source venv/bin/activate
pip install -r requirements 
```

## Docs

There are 3 parts to this API.

- [ABI Documentation]()

> The ABI consists of the outline, or design, of the overall project. This design defines the interface for **all** REST API's within this repository.

- [Core Documentation]()

> The Core is the implementation of the ABI which is used to communicate with the intended REST API.

- [Middleware Documentation]()

> The middleware builds on the Core and consists of a modified REST API for simplifying complicated requests through the use of the Factory Pattern.

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
