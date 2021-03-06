# w3rw - A Wrapper for Cryptocurrency Interfaces
# Copyright (C) 2021 teleprint.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from w3rw import Dict

from w3rw.cex.abstract import AbstractClient

from w3rw.cex.coinbase_pro.messenger import Auth
from w3rw.cex.coinbase_pro.messenger import Messenger
from w3rw.cex.coinbase_pro.messenger import Subscriber


class Account(Subscriber):
    def list(self) -> Dict:
        return self.messenger.get('/accounts').json()

    def get(self, account_id: str) -> Dict:
        return self.messenger.get(f'/accounts/{account_id}').json()

    def holds(self, account_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/accounts/{account_id}/holds', data).json()

    def ledger(self, account_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/accounts/{account_id}/ledger', data).json()

    def transfers(self, account_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/accounts/{account_id}/transfers', data).json()


class Coinbase(Subscriber):
    def wallets(self) -> Dict:
        return self.messenger.get('/coinbase-accounts').json()

    def generate_address(self, account_id: str) -> Dict:
        return self.messenger.post(
            f'/coinbase-accounts/{account_id}/addresses').json()

    def deposit_from(self, data: dict) -> Dict:
        return self.messenger.post('/deposits/coinbase-account', data).json()

    def withdraw_to(self, data: dict) -> Dict:
        return self.messenger.post('/withdrawals/coinbase-account', data).json()


class Convert(Subscriber):
    def post(self, data: dict) -> Dict:
        return self.messenger.post('/conversions', data).json()

    def get(self, conversion_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/conversions/{conversion_id}', data).json()


class Currency(Subscriber):
    def list(self) -> Dict:
        return self.messenger.get('/currencies').json()

    def get(self, currency_id: str) -> Dict:
        return self.messenger.get(f'/currencies/{currency_id}').json()


class Transfer(Subscriber):
    def deposit_from(self, data: dict) -> Dict:
        return self.messenger.post('/deposits/payment-method', data).json()

    def methods(self) -> Dict:
        return self.messenger.get('/payment-methods').json()

    def list(self) -> Dict:
        return self.messenger.get('/transfers').json()

    def get(self, transfer_id: str) -> Dict:
        return self.messenger.get(f'/transfers/{transfer_id}').json()

    def withdraw_to_address(self, data: dict) -> Dict:
        return self.messenger.post('/withdrawals/crypto', data)

    def withdraw_estimate(self, data: dict = None) -> Dict:
        return self.messenger.get('/withdrawals/fee-estimate', data).json()

    def withdraw_to(self, data: dict) -> Dict:
        return self.messenger.post('/withdrawals/payment-method', data).json()


class Order(Subscriber):
    def fills(self, data: dict) -> Dict:
        return self.messenger.get('/fills', data).json()

    def list(self, data: dict) -> Dict:
        return self.messenger.get('/orders', data).json()

    def cancel_all(self, data: dict = None) -> Dict:
        return self.messenger.delete('/orders', data).json()

    def post(self, data: dict) -> Dict:
        return self.messenger.post('/orders', data).json()

    def get(self, order_id: str) -> Dict:
        return self.messenger.get(f'/orders/{order_id}').json()

    def cancel(self, order_id: str, data: dict = None) -> Dict:
        return self.messenger.delete(f'/orders/{order_id}', data).json()


class Oracle(Subscriber):
    def prices(self) -> Dict:
        return self.messenger.get('/oracle')


class Product(Subscriber):
    def list(self) -> Dict:
        return self.messenger.get('/products').json()

    def get(self, product_id: str) -> Dict:
        return self.messenger.get(f'/products/{product_id}').json()

    def book(self, product_id: str, data: dict = None) -> dict:
        return self.messenger.get(
            f'/products/{product_id}/book', data).json()

    def ticker(self, product_id: str) -> Dict:
        return self.messenger.get(f'/products/{product_id}/ticker').json()

    def trades(self, product_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/products/{product_id}/trades', data).json()

    def candles(self, product_id: str, data: dict = None) -> Dict:
        return self.messenger.get(
            f'/products/{product_id}/candles', data).json()

    def stats(self, product_id: str) -> Dict:
        return self.messenger.get(f'/products/{product_id}/stats').json()


class Profile(Subscriber):
    def list(self, data: dict = None) -> Dict:
        return self.messenger.get('/profiles', data).json()

    def create(self, data: dict) -> Dict:
        return self.messenger.post('/profiles', data).json()

    def transfer(self, data: dict) -> Dict:
        return self.messenger.post('/profiles/transfer', data).json()

    def get(self, profile_id: str, data: dict) -> Dict:
        return self.messenger.get(f'/profiles/{profile_id}', data).json()

    def rename(self, profile_id: str, data: dict) -> Dict:
        return self.messenger.put(f'/profiles/{profile_id}', data).json()

    def delete(self, profile_id: str, data: dict) -> Dict:
        return self.messenger.put(
            f'/profiles/{profile_id}/deactivate', data).json()


class Report(Subscriber):
    def list(self, data: dict = None) -> Dict:
        return self.messenger.get('/reports', data).json()

    def create(self, data: dict) -> Dict:
        return self.messenger.post('/reports', data).json()

    def get(self, report_id: str) -> Dict:
        return self.messenger.get(f'/reports/{report_id}').json()


class User(Subscriber):
    def limits(self, user_id: str) -> Dict:
        return self.messenger.get(f'/users/{user_id}/exchange-limits').json()


class Time(Subscriber):
    def get(self) -> Dict:
        # NOTE: The `epoch` field represents decimal seconds since Unix Epoch
        return self.messenger.get('/time').json()


class Client(AbstractClient):
    def __init__(self, messenger: Messenger):
        self.__messenger = messenger

        self.account = Account(messenger)
        self.coinbase = Coinbase(messenger)
        self.convert = Convert(messenger)
        self.currency = Currency(messenger)
        self.transfer = Transfer(messenger)
        self.order = Order(messenger)
        self.oracle = Oracle(messenger)
        self.product = Product(messenger)
        self.profile = Profile(messenger)
        self.report = Report(messenger)
        self.user = User(messenger)
        self.time = Time(messenger)

    @property
    def label(self):
        return 'coinbase_pro'

    @property
    def messenger(self):
        return self.__messenger


def get_messenger(key: str = None,
                  secret: str = None,
                  passphrase: str = None) -> Messenger:

    return Messenger(Auth(key, secret, passphrase))


def get_client(key: str = None,
               secret: str = None,
               passphrase: str = None) -> Client:

    return Client(Messenger(Auth(key, secret, passphrase)))
