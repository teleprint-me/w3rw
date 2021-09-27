import requests
import typing

__agent__: str = 'teleprint.me'
__source__: str = 'https://github.com/teleprint-me/ledger'
__version__: str = '0.1.29'

__offset__: int = 50
__limit__: int = 250
__timeout__: float = 0.275

List = typing.TypeVar('List', list, list[dict])
Dict = typing.TypeVar('Dict', dict, List)
Response = typing.TypeVar('Response', requests.Response, list[requests.Response])
