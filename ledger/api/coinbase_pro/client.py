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

from ledger.api.coinbase_pro.auth import Auth

from ledger.api.coinbase_pro.messenger import Query
from ledger.api.coinbase_pro.messenger import Messenger

from ledger.api.coinbase_pro.context import ProductsContext
from ledger.api.coinbase_pro.context import AccountsBalanceContext
from ledger.api.coinbase_pro.context import AccountsIdentityContext
from ledger.api.coinbase_pro.context import HistoryContext
from ledger.api.coinbase_pro.context import TransfersContext
from ledger.api.coinbase_pro.context import TransfersAccountsContext
from ledger.api.coinbase_pro.context import PriceContext
from ledger.api.coinbase_pro.context import OrderContext


class CoinbaseProClient(AbstractClient):
    def __init__(self, messenger: AbstractMessenger):
        self.__messenger = messenger
        self.__name = 'coinbase-pro'

    @property
    def name(self) -> str:
        return self.__name

    @property
    def messenger(self) -> AbstractMessenger:
        return self.__messenger

    def products(self) -> Dict:
        query = Query('/products')
        response = self.messenger.get(query)
        context = ProductsContext(response)
        return context.data

    def accounts(self) -> Dict:
        query = Query('/accounts')
        response = self.messenger.get(query)
        context = AccountsBalanceContext(response)
        return context.data

    def history(self, product_id: str) -> Dict:
        query = Query('/fills', {'product_id': product_id})
        responses = self.messenger.page(query)
        context = HistoryContext(responses, product_id)
        return context.data

    def deposits(self, product_id: str) -> Dict:
        accounts = AccountsIdentityContext(
            self.messenger.get(Query('/accounts')), product_id
        )
        transfers = TransfersContext(
            self.messenger.page(Query('/transfers', {'type': 'deposit'}))
        )
        context = TransfersAccountsContext(accounts, transfers)
        return context.data

    def withdrawals(self, product_id: str) -> Dict:
        accounts = AccountsIdentityContext(
            self.messenger.get(Query('/accounts')), product_id
        )
        transfers = TransfersContext(
            self.messenger.page(Query('/transfers', {'type': 'withdraw'}))
        )
        context = TransfersAccountsContext(accounts, transfers)
        return context.data

    def price(self, product_id: str) -> dict:
        query = Query(f'/products/{product_id}/ticker')
        response = self.messenger.get(query)
        context = PriceContext(response)
        return context.data

    def order(self, data: dict) -> dict:
        query = Query('/orders', data)
        response = self.messenger.post(query)
        context = OrderContext(response)
        return context.data


class CoinbaseProFactory(AbstractFactory):
    def get_client(self,
                   key: str,
                   secret: str,
                   passphrase: str = None) -> AbstractClient:

        auth = Auth(key, secret, passphrase)
        messenger = Messenger(auth)
        return CoinbaseProClient(messenger)
