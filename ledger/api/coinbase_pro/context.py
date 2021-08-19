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
from ledger.api.factory import List
from ledger.api.factory import Response

from ledger.api.factory import AbstractContext
from ledger.api.factory import AbstractQuery
from ledger.api.factory import AbstractMessenger

import dataclasses
import requests


@dataclasses.dataclass
class Context(AbstractContext):
    __response: Response
    __id: str = None

    @property
    def response(self) -> Response:
        return self.__response

    @response.setter
    def response(self, value: Response):
        self.__response = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    def error(self) -> bool:
        return 200 != self.response.status_code


class PageContext(Context):
    def error(self, response: requests.Response) -> bool:
        return 200 != response.status_code

    @property
    def data(self) -> List:
        collection = []
        for response in self.response:
            data = response.json()
            if self.error(response):
                return [data]
            for result in self.get(data):
                collection.append(result)
        return collection


class ProductsContext(Context):
    @property
    def data(self) -> List:
        response = self.response.json()
        return response if self.error() else [
            {'id': item.get('id'),
             'display': item.get('display_name'),
             'name': item.get('base_currency'),
             'min-size': item.get('min_market_funds')
             } for item in response]


class AccountsBalanceContext(Context):
    @property
    def data(self) -> List:
        response = self.response.json()
        return response if self.error() else [
            {'name': item.get('currency'),
             'balance': item.get('available')
             } for item in response if float(item.get('available')) > 0]


class AccountsIdentityContext(Context):
    @property
    def data(self) -> List:
        response = self.response.json()
        return response if self.error() else [
            {'id': item.get('id'),
             'name': item.get('currency')
             } for item in response
            if item.get('currency') in self.id.split('-')[0]]


class HistoryContext(PageContext):
    def get(self, data: List) -> object:
        for item in data:
            yield {
                'id': item.get('product_id'),
                'side': item.get('side'),
                'price': item.get('price'),
                'size': item.get('size'),
                'timestamp': item.get('created_at')
            }


class TransfersContext(PageContext):
    def get(self, data: List) -> object:
        for item in data:
            yield {
                'id': item.get('account_id'),
                'type': item.get('type'),
                'amount': item.get('amount'),
                'details': item.get('details'),
                'timestamp': item.get('created_at'),
                'canceled': bool(item.get('canceled_at'))
            }


@dataclasses.dataclass
class TransfersAccountsContext(object):
    __accounts: Context
    __transfers: PageContext

    @property
    def accounts(self) -> Context:
        return self.__accounts

    @property
    def transfers(self) -> PageContext:
        return self.__transfers

    @property
    def data(self) -> List:
        collection = []
        for account in self.accounts.data:
            for transfer in self.transfers.data:
                if self.match(account, transfer):
                    collection.append({
                        'type': transfer.get('type'),
                        'name': account.get('name'),
                        'amount': transfer.get('amount'),
                        'fee': self.fee(transfer),
                        'timestamp': transfer.get('timestamp')
                    })
        return collection

    def error(self) -> bool:
        return self.accounts.error() and \
            not self.transfers.data[0].get('message')

    @staticmethod
    def match(account: dict, transfer: dict) -> bool:
        return not transfer.get('canceled') and \
            account.get('id') == transfer.get('id')

    @staticmethod
    def fee(transfer: dict) -> str:
        try:
            return transfer['details']['fee']
        except (KeyError,):
            return '0'


class PriceContext(Context):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error() else {
            'bid': response['bid'],
            'ask': response['ask'],
            'price': response['price']
        }


class OrderContext(Context):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error else {
            'id': response['product_id'],
            'side': response['side'],
            'price': response['price'],
            'size': response['size'],
            'timestamp': response['created_at']
        }
