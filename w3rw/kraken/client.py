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
from w3rw import Dict

from w3rw.factory import AbstractMessenger
from w3rw.factory import AbstractClient
from w3rw.factory import AbstractFactory

from w3rw.kraken.auth import Auth
from w3rw.kraken.messenger import Messenger

from w3rw.kraken.context import ProductsContext
from w3rw.kraken.context import AccountsContext
from w3rw.kraken.context import HistoryContext
from w3rw.kraken.context import TransfersContext
from w3rw.kraken.context import PriceContext
from w3rw.kraken.context import AddOrderContext
from w3rw.kraken.context import QueryOrderContext


class Client(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__name = 'kraken'
        self.__messenger = messenger

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def products(self) -> Dict:
        response = self.messenger.get('/public/AssetPairs')
        context = ProductsContext(response)
        return context.data

    def accounts(self) -> Dict:
        response = self.messenger.post('/private/Balance')
        context = AccountsContext(response)
        return context.data

    def history(self, product_id: str) -> Dict:
        response = self.messenger.page('/private/TradesHistory')
        context = HistoryContext(response, product_id)
        return context.data

    def deposits(self, product_id: str) -> Dict:
        response = self.messenger.page('/private/Ledgers', {'type': 'deposit'})
        context = TransfersContext(response, product_id)
        return context.data

    def withdrawals(self, product_id: str) -> Dict:
        response = self.messenger.page('/private/Ledgers', {'type': 'withdrawal'})
        context = TransfersContext(response, product_id)
        return context.data

    def price(self, product_id: str) -> dict:
        response = self.messenger.get('/public/Ticker', {'pair': product_id})
        context = PriceContext(response, product_id)
        return context.data

    def order(self, data: dict) -> dict:
        response = self.messenger.post('/private/AddOrder', data)
        add_order = AddOrderContext(response)
        response = self.messenger.post('/private/QueryOrders', {'txid': add_order.data})
        query_order = QueryOrderContext(response, add_order.data)
        return query_order.data


class KrakenFactory(AbstractFactory):
    def get_messenger(self, key: str, secret: str) -> AbstractMessenger:
        return Messenger(Auth(key, secret))

    def get_client(self, key: str, secret: str) -> AbstractClient:
        return Client(Messenger(Auth(key, secret)))
