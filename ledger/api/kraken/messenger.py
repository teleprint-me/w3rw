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
from ledger.api.factory import __offset__
from ledger.api.factory import __limit__
from ledger.api.factory import __timeout__
from ledger.api.factory import AbstractAuth
from ledger.api.factory import AbstractAPI
from ledger.api.factory import AbstractQuery
from ledger.api.factory import AbstractMessenger

import requests
import time


class Query(AbstractQuery):
    def __init__(self, endpoint: str, data: dict = None):
        self.__endpoint = endpoint
        self.__data = data if data else {}
        self.__product_id = ''
        self.__callback = lambda default: None

    @property
    def endpoint(self) -> str:
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value: str):
        self.__endpoint = value

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def product_id(self) -> str:
        return self.__product_id

    @product_id.setter
    def product_id(self, value: str):
        self.__product_id = value

    @property
    def callback(self) -> object:
        return self.__callback

    @callback.setter
    def callback(self, value: object):
        self.__callback = value


class API(AbstractAPI):
    @property
    def version(self) -> int:
        return 0

    @property
    def url(self) -> str:
        return 'https://api.kraken.com'

    def endpoint(self, value: str) -> str:
        if value.startswith(f'/{self.version}'):
            return value
        return f'/{self.version}/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Messenger(AbstractMessenger):
    def __init__(self, auth: AbstractAuth = None) -> None:
        self.__auth = auth
        self.__api = API()
        self.__timeout = 30
        self.__session = requests.Session()

    @property
    def auth(self) -> AbstractAuth:
        return self.__auth

    @property
    def api(self) -> API:
        return self.__api

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def session(self) -> requests.Session:
        return self.__session

    def get(self, query: AbstractQuery) -> requests.Response:
        time.sleep(__timeout__)
        url = self.api.path(query.endpoint)
        query.endpoint = self.api.endpoint(query.endpoint)
        query.data['nonce'] = self.auth.nonce
        return self.session.get(
            url,
            params=query.data,
            headers=self.auth(query),
            timeout=self.timeout
        )

    def post(self, query: AbstractQuery) -> requests.Response:
        time.sleep(__timeout__)
        url = self.api.path(query.endpoint)
        query.endpoint = self.api.endpoint(query.endpoint)
        query.data['nonce'] = self.auth.nonce
        return self.session.post(
            url,
            data=query.data,
            headers=self.auth(query),
            timeout=self.timeout
        )

    def page(self, query: AbstractQuery) -> object:
        query.data['ofs'] = 0
        while query.data['ofs'] < __limit__:
            response = self.post(query)
            if 200 != response.status_code:
                return response.json()
            for item in query.callback(query.product_id, response):
                yield item
            query.data['ofs'] += __offset__

    def close(self) -> None:
        self.session.close()
