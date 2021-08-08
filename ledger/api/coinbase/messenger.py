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
from ledger.api.factory import AbstractAPI
from ledger.api.factory import AbstractMessenger

from ledger.api.coinbase.auth import Auth

import requests


class API(AbstractAPI):
    def __init__(self):
        self.__options = {}

    @property
    def version(self) -> int:
        return 2

    @property
    def options(self) -> dict:
        return self.__options

    @options.setter
    def options(self, value: dict) -> None:
        """set the dictionary for response.json"""
        assert isinstance(value, dict), '`value` must be of type dict'
        self.__options = value

    @property
    def url(self) -> str:
        return 'https://api.coinbase.com'

    def endpoint(self, value: str) -> str:
        return f'/v{self.version}/{value.lstrip("/")}'

    def path(self, value: str) -> str:
        return f'{self.url}/{self.endpoint(value).lstrip("/")}'


class Messenger(AbstractMessenger):
    def __init__(self, auth: Auth = None) -> None:
        self.__auth = auth
        self.__api = API()
        self.__timeout = 30
        self.__session = requests.Session()
        self.__response = None

    @property
    def auth(self) -> Auth:
        return self.__auth

    @property
    def api(self) -> API:
        return self.__api

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def options(self) -> dict:
        return self.__api.options

    @options.setter
    def options(self, value: dict) -> None:
        self.__api.options = value

    @property
    def session(self) -> requests.Session:
        return self.__session

    @property
    def response(self) -> requests.Response:
        return self.__response

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = self.__api.path(endpoint)

        self.__response = self.session.get(
            url,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        )

        return self.__response.json(**self.options)

    def post(self, endpoint: str, data: dict = None) -> dict:
        url = self.__api.path(endpoint)

        self.__response = self.session.post(
            url,
            json=data,
            auth=self.auth,
            timeout=self.timeout
        )

        return self.__response.json(**self.options)

    def page(self, endpoint: str, params: dict = None) -> object:
        # source: https://docs.pro.coinbase.com/?python#pagination
        url = self.__api.path(endpoint)

        if params is None:
            params = dict()

        while True:
            self.__response = self.session.get(
                url,
                params=params,
                auth=self.auth,
                timeout=self.timeout
            )

            results = self.__response.json(**self.options)

            if self.__response.status_code != 200:
                return results

            for result in results:
                yield result

            after = self.__response.headers.get('CB-AFTER')
            before = params.get('before')
            end = not after or before

            if end:
                break

            params['after'] = self.__response.headers['CB-AFTER']

    def close(self):
        self.session.close()
