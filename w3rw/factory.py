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
from w3rw import Response

import abc
import requests


class AbstractAuth(abc.ABC):
    @abc.abstractmethod
    def __init__(self, key: str, secret: str):
        pass


class AbstractAPI(abc.ABC):
    @abc.abstractproperty
    def version(self) -> int:
        """return the current rest api version"""
        pass

    @abc.abstractproperty
    def url(self) -> str:
        """return the rest api url"""
        pass

    @abc.abstractmethod
    def endpoint(self, value: str) -> str:
        """return a endpoint based on `value`"""
        pass

    @abc.abstractmethod
    def path(self, value: str) -> str:
        """return the full path based on url and endpoint `value`"""
        pass


class AbstractMessenger(abc.ABC):
    @abc.abstractmethod
    def __init__(self, auth: AbstractAuth):
        pass

    @abc.abstractproperty
    def api(self) -> AbstractAPI:
        pass

    @abc.abstractproperty
    def auth(self) -> AbstractAuth:
        pass

    @abc.abstractproperty
    def session(self) -> requests.Session:
        pass

    @abc.abstractproperty
    def timeout(self) -> int:
        pass

    @abc.abstractmethod
    def get(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abc.abstractmethod
    def post(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abc.abstractmethod
    def page(self, endpoint: str, data: dict = None) -> Response:
        pass

    @abc.abstractmethod
    def close(self) -> None:
        pass


class AbstractContext(abc.ABC):
    @abc.abstractproperty
    def response(self) -> Response:
        pass

    @abc.abstractproperty
    def id(self) -> str:
        pass

    @abc.abstractmethod
    def data(self) -> Dict:
        pass

    @abc.abstractmethod
    def error(self) -> bool:
        pass


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass

    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def messenger(self) -> AbstractMessenger:
        pass

    @abc.abstractmethod
    def products(self) -> Dict:
        pass

    @abc.abstractmethod
    def accounts(self) -> Dict:
        pass

    @abc.abstractmethod
    def history(self, product_id: str) -> Dict:
        pass

    @abc.abstractmethod
    def deposits(self, product_id: str) -> Dict:
        pass

    @abc.abstractmethod
    def withdrawals(self, product_id: str) -> Dict:
        pass

    @abc.abstractmethod
    def price(self, product_id: str) -> dict:
        pass

    @abc.abstractmethod
    def order(self, data: dict) -> dict:
        pass


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def get_messenger(self, key: str, secret: str) -> AbstractMessenger:
        pass

    @abc.abstractmethod
    def get_client(self, key: str, secret: str) -> AbstractClient:
        pass
