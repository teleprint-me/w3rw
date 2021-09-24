# Install

## Notes

- This library is intentionally minimalist and targets only REST API's.
- This library is a work in progress and is subject to change. 
- There may be aspects of this library that are broken, buggy, or missing from the implementation.
- There is NO WARRANTY, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.


## Consumers

```sh
mkdir /my/project/path 
cd /my/project/path
virtualenv venv 
source venv/bin/activate
pip install git+https://github.com/teleprint-me/ledger-api.git#egg=w3rw
```

## Manual

```sh
mkdir /my/project/path
git clone https://github.com/teleprint-me/ledger-api.git /my/project/path/w3rw
cd /my/project/path
virtualenv venv 
source venv/bin/activate
cd /my/project/path/w3rw
python setup.py install
```

## Developers

```sh
git clone https://github.com/teleprint-me/ledger-api.git /my/project/path/w3rw
cd /my/project/path/w3rw
virtualenv venv 
source venv/bin/activate
pip install -r requirements-dev.txt
touch settings.ini main.py
```

_Note: A [GPG Signature](https://docs.github.com/en/authentication/managing-commit-signature-verification) is required to make a Pull Request._
