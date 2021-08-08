# Ledger - A web application to track cryptocurrency investments
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
from ledger.api.factory import AbstractMessenger
from ledger.api.factory import AbstractClient
from ledger.api.factory import AbstractFactory

from ledger.api.cbpro.auth import Auth
from ledger.api.cbpro.messenger import Messenger

from time import sleep


def on_error(response) -> bool:
    if isinstance(response, dict):
        return bool(response.get('message'))
    return False


def get_fee(transfer: dict) -> str:
    has_fee = 'details' in transfer and 'fee' in transfer['details']
    return transfer['details']['fee'] if has_fee else '0'


def has_product(asset: str, transfer: dict, account: dict) -> bool:
    product = account['currency'] in asset.split('-')[0]
    matched = account['id'] == transfer['account_id']
    canceled = transfer['canceled_at'] is not None
    return product and matched and not canceled


def get_product(transfer: dict, account: dict) -> dict:
    return {
        'type': transfer['type'],
        'currency': account['currency'],
        'amount': transfer['amount'],
        'fee': get_fee(transfer),
        'timestamp': transfer['created_at']
    }


def get_transfers(asset, transfers, accounts) -> list:
    products = []
    for transfer in transfers:
        for account in accounts:
            full = asset == 'all'
            search = has_product(asset, transfer, account)
            if full or search:
                products.append(get_product(transfer, account))
    return products


class CoinbaseProClient(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__name = 'coinbase-pro'
        self.__messenger = messenger

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def get_assets(self) -> list:
        response = self.messenger.get('/products')
        if on_error(response):
            return response
        return [{
                'id': asset['id'],
                'display': asset['display_name'],
                'name': asset['base_currency'],
                'min-size': asset['min_market_funds']
                } for asset in response]

    def get_accounts(self) -> list:
        response = self.messenger.get('/accounts')
        if on_error(response):
            return response
        return [{
                'name': account['currency'],
                'balance': account['available']
                } for account in response if float(account['available']) > 0]

    def get_history(self, asset: str) -> list:
        response = self.messenger.page('/fills', {'product_id': asset})
        if on_error(response):
            return response
        return [{
                'id': fill['product_id'],
                'side': fill['side'],
                'price': fill['price'],
                'size': fill['size'],
                'timestamp': fill['created_at']
                } for fill in response]

    def get_deposits(self, asset: str) -> list:
        transfers = self.messenger.page('/transfers', {'type': 'deposit'})
        if on_error(transfers):
            return transfers
        sleep(0.25)
        accounts = self.messenger.get('/accounts')
        if on_error(accounts):
            return accounts
        return get_transfers(asset, transfers, accounts)

    def get_withdrawals(self, asset: str) -> list:
        transfers = self.messenger.page('/transfers', {'type': 'withdraw'})
        if on_error(transfers):
            return transfers
        sleep(0.25)
        accounts = self.messenger.get('/accounts')
        if on_error(accounts):
            return accounts
        return get_transfers(asset, transfers, accounts)

    def get_price(self, asset: str) -> dict:
        response = self.messenger.get(f'/products/{asset}/ticker')
        return {
            'bid': response['bid'],
            'ask': response['ask'],
            'price': response['price']
        }

    def post_order(self, data: dict) -> dict:
        # TODO: Filter out redundent data
        response = self.messenger.post('/orders', data)
        return {
            'timestamp': response['created_at'],
            'id': response['product_id'],
            'side': response['side'],
            'price': response['price'],
            'size': response['size']
        }


class CoinbaseProFactory(AbstractFactory):
    def get_client(self,
                   key: str,
                   secret: str,
                   passphrase: str) -> AbstractClient:

        auth = Auth(key, secret, passphrase)
        messenger = Messenger(auth)
        return CoinbaseProClient(messenger)
