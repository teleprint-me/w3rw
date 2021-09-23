# Web3 Requests Wrapper

```
          _____
__      _|___ / _ ____      __
\ \ /\ / / |_ \| '__\ \ /\ / /
 \ V  V / ___) | |   \ V  V /
  \_/\_/ |____/|_|    \_/\_/
```

## About

A wrapper for interfacing with Centralized and Decentralized Cryptocurrency Application Programming Interfaces.

## Docs

- [Install](https://github.com/teleprint-me/ledger-api/tree/main/docs)

    Install the w3rw library

- [ABI](https://github.com/teleprint-me/ledger-api/blob/main/docs/ABI.md)

    The ABI consists of the general design which defines the general interface for this repository.

- [Core](https://github.com/teleprint-me/ledger-api/blob/main/docs/Core.md)

    The Core is the implementation of the ABI which is used to communicate with the intended interface.

- [Middleware](https://github.com/teleprint-me/ledger-api/blob/main/docs/Middleware.md)

    The middleware builds on the Core and consists of a modified interface for simplifying complicated requests.

## Tips

- Bitcoin (Segwit): 3E1YSahzUnYYx2RTuRt4KWogDBCsdCS1n3
- Ethereum: 0x7be933221135468b9886632771fF289341144C3a
- Litecoin (Segwit): MMNDfhgc3jfs3XJoJ7DSCedBp742dH12jD

## TODO

### Documentation

- [ ] ABI
- [ ] Core
- [ ] Middleware

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

#### A Note on Testing

There is no method to gaurentee testing. Only a guarentee to verify code integrity. Testing these API's is difficult seeing as some do not support a sandbox for testing. The major pitfall to this is that exploratory testing is required to verify that the code is functioning as intended. This makes bugs difficult to pinpoint. If testing is implemented at any point in time, then it should be implemented to verify the structure of the code instead.
