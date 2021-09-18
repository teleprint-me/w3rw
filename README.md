# teleprint.me rest api

## About

A `requests` wrapper for interfacing with Centralized and Decentralized Cryptocurrency REST API's.

## Notes

- This library is a dependency of the [teleprint-me/ledger](https://github.com/teleprint-me/ledger) repository.
- This library is intentionally minimalist and should stay as such. Adding features is left as the responsibility to the developer.
- There is no plan to add Web Socket support. There are plenty of libraries that can help you achieve this end. The `websocket-client` library is a popular choice.
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

- [ABI Documentation](https://github.com/teleprint-me/ledger-api/blob/main/docs/README.md)

    The ABI consists of the outline, or design, of the overall project. This design defines the interface for **all** REST API's within this repository.

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

_Note: There is no method to gaurentee testing. Only a guarentee to verify code integrity. Testing these API's is difficult seeing as some do not support a sandbox for testing. An example of this is Kraken. Kraken does not support a sandbox and there is no way to validate that certain endpoints are functioning as expected. Another caveat is that Kraken does not utilize the HTTP response methods such as the 200 Success Code. You have to manually check the response for a error key. This makes it even more difficult seeing as checking for a 200 response code is the expected method for a successful response. The major pitfall to this is that exploratory testing is required to make sure the code is functioning as expected making bugs difficult to pinpoint. Testing may not be implemented for this library for this very reason and this reason alone. If testing is implemented at any point in time, then it should be implemented to verify the structure of the code instead. It's an unfortunate compromise that makes this a challenging experience._
