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
from ledger.api.factory import Dict
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
from ledger.api.kraken.context import AddOrderContext
from ledger.api.kraken.context import QueryOrderContext


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
        query = Query('/public/AssetPairs')
        response = self.messenger.get(query)
        context = ProductsContext(response)
        return context.data

    def accounts(self) -> Dict:
        query = Query('/private/Balance')
        response = self.messenger.post(query)
        context = AccountsContext(response)
        return context.data

    def history(self, product_id: str) -> Dict:
        query = Query('/private/TradesHistory')
        response = self.messenger.page(query)
        context = HistoryContext(response, product_id)
        return context.data

    def deposits(self, product_id: str) -> Dict:
        query = Query('/private/Ledgers', {'type': 'deposit'})
        response = self.messenger.page(query)
        context = TransfersContext(response, product_id)
        return context.data

    def withdrawals(self, product_id: str) -> Dict:
        query = Query('/private/Ledgers', {'type': 'withdrawal'})
        response = self.messenger.page(query)
        context = TransfersContext(response, product_id)
        return context.data

    def price(self, product_id: str) -> dict:
        query = Query('/public/Ticker', {'pair': product_id})
        response = self.messenger.get(query)
        context = PriceContext(response, product_id)
        return context.data

    def order(self, data: dict) -> dict:
        response = self.messenger.post(Query('/private/AddOrder', data))
        add_order = AddOrderContext(response)
        query = Query('/private/QueryOrders', {'txid': add_order.data})
        response = self.messenger.post(query)
        query_order = QueryOrderContext(response, add_order.data)
        return query_order.data


class KrakenFactory(AbstractFactory):
    def get_client(self, key: str, secret: str) -> AbstractClient:
        auth = Auth(key, secret)
        messenger = Messenger(auth)
        return Client(messenger)
