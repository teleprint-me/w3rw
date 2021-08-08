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
from ledger.api.factory import AbstractQuery
from ledger.api.factory import AbstractMessenger
from ledger.api.factory import AbstractContext

import requests


class GetContext(AbstractContext):
    def __init__(self, query: AbstractQuery, messenger: AbstractMessenger):
        self.__query = query
        self.__response = messenger.get(query)

    @property
    def query(self) -> AbstractQuery:
        return self.__query

    @property
    def response(self) -> requests.Response:
        return self.__response

    @property
    def error(self) -> bool:
        return self.response.status_code != 200

    @property
    def data(self) -> object:
        return None


class PostContext(GetContext):
    def __init__(self, query: AbstractQuery, messenger: AbstractMessenger):
        self.__query = query
        self.__response = messenger.post(query)


class PageContext(GetContext):
    def __init__(self, query: AbstractQuery, messenger: AbstractMessenger):
        self.__query = query
        self.__response = messenger.page(query)


class ProductsContext(GetContext):
    @property
    def data(self) -> list:
        response = self.response.json()
        return response if self.error else [
            {'id': item.get('id'),
             'display': item.get('display_name'),
             'name': item.get('base_currency'),
             'min-size': item.get('min_market_funds')
             } for item in response]


class AccountsContext(GetContext):
    @property
    def data(self) -> list:
        response = self.response.json()
        return response if self.error else [
            {'name': item.get('currency'),
             'balance': item.get('available')
             } for item in response if float(item['available']) > 0]


class HistoryContext(PageContext):
    @property
    def data(self) -> list:
        response = self.response.json()
        return response if self.error else [
            {'id': item.get('product_id'),
             'side': item.get('side'),
             'price': item.get('price'),
             'size': item.get('size'),
             'timestamp': item.get('created_at')
             } for item in response]


class TransfersContext(PageContext):
    def __init__(self, query: AbstractQuery, messenger: AbstractMessenger):
        self.__query = query
        self.__response = messenger.page(query)
        self.__product_id = ''
        self.__accounts = []

    @property
    def product_id(self) -> str:
        return self.__product_id

    @product_id.setter
    def product_id(self, value: str):
        self.__product_id = value

    @property
    def accounts(self) -> list:
        return self.__accounts

    @accounts.setter
    def accounts(self, value: list):
        self.__accounts = value

    @property
    def data(self) -> list:
        products = []
        response = self.response.json()
        if self.error:
            return response
        for transfer in response:
            for account in self.accounts:
                if self.match(account, transfer):
                    product = self.format(account, transfer)
                    products.append(product)
        return products

    @staticmethod
    def fee(transfer: dict) -> str:
        try:
            return transfer['details']['fee']
        except (KeyError,):
            return '0'

    @staticmethod
    def is_canceled(transfer) -> bool:
        return bool(transfer.get('canceled_at'))

    @staticmethod
    def is_matched(account: dict, transfer: dict) -> bool:
        return account.get('id') == transfer.get('account_id')

    def is_product(self, account: dict) -> bool:
        return account.get('currency') in self.product_id.split('-')[0]

    def match(self, account: dict, transfer: dict) -> bool:
        return self.is_product(account) and \
            self.is_matched(account, transfer) and \
            not self.is_canceled(transfer)

    def format(self, account: dict, transfer: dict) -> dict:
        return {
            'type': transfer['type'],
            'name': account['currency'],
            'amount': transfer['amount'],
            'fee': self.fee(transfer),
            'timestamp': transfer['created_at']
        }


class PriceContext(GetContext):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error else {
            'bid': response['bid'],
            'ask': response['ask'],
            'price': response['price']
        }


class OrderContext(PostContext):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error else {
            'timestamp': response['created_at'],
            'id': response['product_id'],
            'side': response['side'],
            'price': response['price'],
            'size': response['size']
        }
