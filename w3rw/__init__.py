import requests
import typing

__agent__: str = 'w3rw'
__source__: str = 'https://github.com/teleprint-me/w3rw'
__version__: str = '0.2.4'

__offset__: int = 50
__limit__: int = 250
__timeout__: float = 1 / 3.5

List = typing.TypeVar('List', list, list[dict])
Dict = typing.TypeVar('Dict', dict, List)

Response = typing.TypeVar('Response', requests.Response, list[requests.Response])
