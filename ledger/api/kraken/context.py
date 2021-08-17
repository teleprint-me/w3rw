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

import dataclasses
import datetime
import requests


def epoch_to_datetime(timestamp: float) -> str:
    '''convert timestamp from epoch to iso 8601'''
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.isoformat()


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
        return bool(self.response.json()['error'])


class PageContext(Context):
    def error(self, response: requests.Response) -> bool:
        ok = 200 == response.status_code
        error = bool(response.json()['error'])
        return not ok or error

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
        return [response] if self.error() else [
            {'id': k,
             'display': v.get('wsname'),
             'name': v.get('base'),
             'min-size': v.get('ordermin')
             } for k, v in response['result'].items()]


class AccountsContext(Context):
    @property
    def data(self) -> List:
        response = self.response.json()
        return [response] if self.error() else [
            {'name': k,
             'balance': v
             } for k, v in response['result'].items() if float(v) > 0]


class HistoryContext(PageContext):
    def get(self, data: dict) -> object:
        for trade in data['result']['trades'].values():
            if trade['pair'] == self.id:
                yield {
                    'id': trade['pair'],
                    'side': trade['type'],
                    'price': trade['price'],
                    'size': trade['vol'],
                    'timestamp': epoch_to_datetime(trade['time'])
                }


class TransfersContext(PageContext):
    def get(self, data: dict) -> object:
        for transfer in data['result']['ledger'].values():
            if transfer['asset'] == self.id.split('Z')[0]:
                yield {
                    'name': transfer['asset'],
                    'type': transfer['type'],
                    'amount': transfer['amount'],
                    'fee': transfer['fee'],
                    'timestamp': epoch_to_datetime(transfer['time'])
                }


class PriceContext(Context):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error() else {
            'bid': response['result'][self.id]['b'][0],
            'ask': response['result'][self.id]['a'][0],
            'price': response['result'][self.id]['p'][0]
        }


class AddOrderContext(Context):
    @property
    def data(self) -> str:
        response = self.response.json()
        return response if self.error() else response['result']['txid']


class QueryOrderContext(Context):
    @property
    def data(self) -> dict:
        response = self.response.json()
        return response if self.error() else {
            'id': response['result'][self.id]['descr']['pair'],
            'side': response['result'][self.id]['descr']['type'],
            'price': response['result'][self.id]['price'],
            'size': response['result'][self.id]['vol'],
            'timestamp': epoch_to_datetime(response['result'][self.id]['opentm'])
        }
