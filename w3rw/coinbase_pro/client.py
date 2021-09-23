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

from w3rw.coinbase_pro.auth import Auth
from w3rw.coinbase_pro.messenger import Messenger

from w3rw.coinbase_pro.context import ProductsContext
from w3rw.coinbase_pro.context import AccountsBalanceContext
from w3rw.coinbase_pro.context import AccountsIdentityContext
from w3rw.coinbase_pro.context import HistoryContext
from w3rw.coinbase_pro.context import TransfersContext
from w3rw.coinbase_pro.context import TransfersAccountsContext
from w3rw.coinbase_pro.context import PriceContext
from w3rw.coinbase_pro.context import OrderContext


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
        response = self.messenger.get('/products')
        context = ProductsContext(response)
        return context.data

    def accounts(self) -> Dict:
        response = self.messenger.get('/accounts')
        context = AccountsBalanceContext(response)
        return context.data

    def history(self, product_id: str) -> Dict:
        responses = self.messenger.page(
            '/fills', {'product_id': product_id}
        )
        context = HistoryContext(responses, product_id)
        return context.data

    def deposits(self, product_id: str) -> Dict:
        accounts = AccountsIdentityContext(
            self.messenger.get('/accounts'), product_id
        )
        transfers = TransfersContext(
            self.messenger.page('/transfers', {'type': 'deposit'})
        )
        context = TransfersAccountsContext(accounts, transfers)
        return context.data

    def withdrawals(self, product_id: str) -> Dict:
        accounts = AccountsIdentityContext(
            self.messenger.get('/accounts'), product_id
        )
        transfers = TransfersContext(
            self.messenger.page('/transfers', {'type': 'withdraw'})
        )
        context = TransfersAccountsContext(accounts, transfers)
        return context.data

    def price(self, product_id: str) -> dict:
        response = self.messenger.get(f'/products/{product_id}/ticker')
        context = PriceContext(response)
        return context.data

    def order(self, json: dict) -> dict:
        response = self.messenger.post('/orders', json)
        context = OrderContext(response)
        return context.data


class CoinbaseProFactory(AbstractFactory):
    def get_messenger(self,
                      key: str,
                      secret: str,
                      passphrase: str = None) -> AbstractClient:

        return Messenger(Auth(key, secret, passphrase))

    def get_client(self,
                   key: str,
                   secret: str,
                   passphrase: str = None) -> AbstractClient:

        return CoinbaseProClient(Messenger(Auth(key, secret, passphrase)))
