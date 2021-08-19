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
from ledger.api.factory import __timeout__

from ledger.api.factory import Response

from ledger.api.factory import AbstractAuth
from ledger.api.factory import AbstractAPI
from ledger.api.factory import AbstractQuery
from ledger.api.factory import AbstractMessenger

import dataclasses
import requests
import time


@dataclasses.dataclass
class Query(AbstractQuery):
    __endpoint: str
    __data: dict = dataclasses.field(default_factory=dict)

    @property
    def endpoint(self) -> str:
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value: str):
        self.__endpoint = value

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, value: dict):
        self.__data = value


@dataclasses.dataclass
class API(AbstractAPI):
    __version: int = 0
    __url: str = 'https://api.pro.coinbase.com'

    @property
    def version(self) -> int:
        return self.__version

    @property
    def url(self) -> str:
        return self.__url

    def endpoint(self, value: str) -> str:
        return f'/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Messenger(AbstractMessenger):
    def __init__(self, auth: AbstractAuth = None):
        self.__auth: AbstractAuth = auth
        self.__api: AbstractAPI = API()
        self.__session: requests.Session = requests.Session()
        self.__timeout: int = 30

    @property
    def auth(self) -> AbstractAuth:
        return self.__auth

    @property
    def api(self) -> AbstractAPI:
        return self.__api

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def session(self) -> requests.Session:
        return self.__session

    def get(self, query: AbstractQuery) -> Response:
        time.sleep(__timeout__)
        return self.session.get(
            self.api.path(query.endpoint),
            params=query.data,
            auth=self.auth,
            timeout=self.timeout
        )

    def post(self, query: AbstractQuery) -> Response:
        time.sleep(__timeout__)
        return self.session.post(
            self.api.path(query.endpoint),
            json=query.data,
            auth=self.auth,
            timeout=self.timeout
        )

    def page(self, query: AbstractQuery) -> Response:
        responses = []
        while True:
            response = self.get(query)
            if 200 != response.status_code:
                return [response]
            if not response.json():
                break
            responses.append(response)
            after = response.headers.get('CB-AFTER')
            before = query.data.get('before')
            if not after or before:
                break
            query.data['after'] = response.headers.get('CB-AFTER')
        return responses

    def close(self):
        self.session.close()
