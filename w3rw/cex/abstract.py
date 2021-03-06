# w3rw - A Wrapper for Cryptocurrency Interfaces
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
from w3rw import Response

from requests import Session

import abc


class AbstractAPI(abc.ABC):
    @abc.abstractproperty
    def version(self) -> int:
        pass

    @abc.abstractproperty
    def url(self) -> str:
        pass

    @abc.abstractmethod
    def endpoint(self, value: str) -> str:
        pass

    @abc.abstractmethod
    def path(self, value: str) -> str:
        pass


class AbstractAuth(abc.ABC):
    @abc.abstractmethod
    def __init__(self, key: str = None, secret: str = None):
        pass

    @abc.abstractmethod
    def __call__(self) -> object:
        pass

    @abc.abstractmethod
    def signature(self) -> object:
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
    def session(self) -> Session:
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


class AbstractSubscriber(abc.ABC):
    @abc.abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass

    @abc.abstractproperty
    def messenger(self) -> AbstractMessenger:
        pass

    @abc.abstractmethod
    def error(self, response: Response) -> bool:
        pass


class AbstractClient(abc.ABC):
    @abc.abstractmethod
    def __init__(self, messenger: AbstractMessenger):
        pass

    @abc.abstractproperty
    def label(self) -> str:
        pass

    @abc.abstractproperty
    def messenger(self) -> AbstractMessenger:
        pass
