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

from ledger.api.kraken.auth import Auth

from ledger.api.kraken.messenger import Query
from ledger.api.kraken.messenger import Messenger

from ledger.api.kraken.context import ProductsContext
from ledger.api.kraken.context import AccountsContext
from ledger.api.kraken.context import HistoryContext
from ledger.api.kraken.context import TransfersContext
from ledger.api.kraken.context import PriceContext
from ledger.api.kraken.context import OrderContext

from datetime import datetime


def on_error(response: object) -> bool:
    return bool(response.get('error'))


def epoch_to_datetime(timestamp: float) -> str:
    '''convert timestamp from epoch to iso 8601'''
    date = datetime.fromtimestamp(timestamp)
    return date.isoformat()


def get_average_price(prices: list) -> str:
    '''return average price based on approx bids and asks at market value'''
    pricelist = sum(float(p) for p in prices) / len(prices)
    return f'{pricelist:.5f}'


def get_history(product_id: str, response: object) -> object:
    for trade in response['result']['trades'].values():
        if trade['pair'] == product_id:
            yield {
                'id': trade['pair'],
                'side': trade['type'],
                'price': trade['price'],
                'size': trade['vol'],
                'timestamp': epoch_to_datetime(trade['time'])
            }


def get_transfers(product_id: str, response: object) -> object:
    for transfer in response['result']['ledger'].values():
        if transfer['asset'] == product_id.split('Z')[0]:
            yield {
                'type': transfer['type'],
                'currency': transfer['asset'],
                'amount': transfer['amount'],
                'fee': transfer['fee'],
                'timestamp': epoch_to_datetime(transfer['time'])
            }


class KrakenClient(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__name = 'kraken'
        self.__messenger = messenger

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def products(self) -> list:
        query = Query('/public/AssetPairs')
        context = ProductsContext(query, self.messenger)
        return context.data

    def accounts(self) -> list:
        query = Query('/private/Balance')
        context = AccountsContext(query, self.messenger)
        return context.data

    def history(self, product_id: str) -> list:
        query = Query('/private/TradesHistory')
        query.product_id = product_id
        query.callback = get_history
        context = HistoryContext(query, self.messenger)
        return context.data

    def deposits(self, asset: str) -> list:
        query = Query('/private/Ledgers', {'type': 'deposit'})
        query.asset = asset
        query.callback = get_transfers
        return self.messenger.page(query)

    def withdrawals(self, asset: str) -> list:
        query = Query('/private/Ledgers', {'type': 'withdrawal'})
        query.asset = asset
        query.callback = get_transfers
        return self.messenger.page(query)

    def price(self, asset: str) -> dict:
        response = self.messenger.get('/public/Ticker', {'pair': asset})
        if self.has_error(response):
            return response['error']
        ticker = response['result'][asset]
        return {
            'bid': ticker['b'][0],
            'ask': ticker['a'][0],
            'price': get_average_price(ticker['p'])
        }

    def order(self, data: dict) -> dict:
        order = self.messenger.post('/private/AddOrder', data)
        if self.has_error(order):
            return order['error']
        txid = order['result']['txid']
        query = self.messenger.post('/private/QueryOrders', {'txid': txid})
        if self.has_error(query):
            return query['error']
        info = query['result'][txid]
        return {
            'id': info['descr']['pair'],
            'side': info['descr']['type'],
            'price': info['price'],
            'size': info['vol'],
            'timestamp': epoch_to_datetime(info['opentm'])
        }


class KrakenFactory(AbstractFactory):
    def get_client(self,
                   key: str,
                   secret: str,
                   passphrase: str = None) -> AbstractClient:

        auth = Auth(key, secret, passphrase)
        messenger = Messenger(auth)
        return KrakenClient(messenger)
