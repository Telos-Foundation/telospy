import logging
import requests
import json
from urllib import parse
from requests.exceptions import ConnectionError
from .util import todict

__all__ = ['WalletAPI', 'ChainAPI', 'wallet_api', 'chain_api', 'configure_chain_api', 'configure_wallet_api']

wallet_api = None
chain_api = None

# TODO: Make wallet_api and chain_api a property to enforce configuration


def configure_wallet_api(url='http://127.0.0.1:8999'):
    assert isinstance(url, str), "Url is not a string"
    global wallet_api
    wallet_api = WalletAPI(url)


def configure_chain_api(url):
    assert isinstance(url, str), "Url is not a string"
    global chain_api
    chain_api = ChainAPI(url)


class API:

    def __init__(self, headers, base_url):
        """Base API class"""
        self.base_headers = headers
        self.base_url = base_url
        self.params = {}
        self.logger = logging.getLogger(__name__)

    def post(self, endpoint, data=None, params={}, headers={}):
        try:
            m_headers = {**self.base_headers, **headers}
            m_params = {**self.params, **params}
            return requests.post(url=parse.urljoin(self.base_url, endpoint), data=data, headers=m_headers, params=m_params)
        except ConnectionError as e:
            raise e
            # TODO: Raise custom exceptions or log accurate error message


class WalletAPI(API):

    def __init__(self, base_url='http://127.0.0.1:8999'):
        """Wallet API for communicating with EOSIO wallet RPCs."""
        headers = {'Accept': 'application/json','Content-Type': 'application/json'}
        API.__init__(self, headers, parse.urljoin(base_url, '/v1/wallet/'))

        self.logger.debug('Constructing %s', __name__)

    def create(self, name):
        try:
            return self.post('create', data="\"%s\"" % name)
        except ConnectionError as e:
            raise e

    def unlock(self, password, name='default'):
        try:
            body = json.dumps([name, password])
            return self.post('unlock', data=body)
        except ConnectionError as e:
            raise e

    def lock(self, name='default'):
        try:
            return self.post('lock', data="\"%s\"" % name)
        except ConnectionError as e:
            raise e

    def list_wallets(self):
        try:
            return self.post('list_wallets')
        except ConnectionError as e:
            raise e

    def list_keys(self, password, name='default'):
        try:
            body = json.dumps([name, password])
            return self.post('list_keys', data=body)
        except ConnectionError as e:
            raise e

    def get_public_keys(self):
        try:
            return self.post('get_public_keys')
        except ConnectionError as e:
            raise e

    def create_key(self, key_type="K1", name="default"):
        try:
            body = json.dumps([name, key_type])
            return self.post('create_key', data=body)
        except ConnectionError as e:
            raise e

    def import_key(self, private_key, name='default'):
        try:
            body = json.dumps([name, private_key])
            return self.post('import_key', data=body)
        except ConnectionError as e:
            raise e

    def set_timeout(self, time_out):
        try:
            return self.post('set_timeout', data=time_out)
        except ConnectionError as e:
            raise e

    def sign_transaction(self, transaction, keys, chain_id=""):
        try:
            body = json.dumps([todict(transaction), keys, chain_id])
            return self.post('sign_transaction', data=body)
        except ConnectionError as e:
            raise e


class ChainAPI(API):

    def __init__(self, base_url):
        """Chain API class for communicating with EOSIO based chain RPCs."""
        headers = {'Accept': 'application/json','Content-Type': 'application/json'}
        API.__init__(self, headers, parse.urljoin(base_url, '/v1/chain/'))

    def get_currency_balance(self, account, code='eosio.token', symbol='TLOS'):
        try:
            body = json.dumps({'code': code, 'account': account, 'symbol': symbol})
            return self.post('get_currency_balance', data=body)
        except ConnectionError as e:
            raise e

    def get_currency_stats(self, account, symbol='TLOS'):
        try:
            body = json.dumps({'code': 'eosio.token', 'account': account, 'symbol': symbol})
            return self.post('get_currency_stats', data=body)
        except ConnectionError as e:
            raise e

    def get_block_header_state(self, block_num):
        try:
            body = json.dumps({'block_num_or_id': block_num})
            return self.post('get_block_header_state', data=body)
        except ConnectionError as e:
            raise e

    def get_info(self):
        try:
            return self.post('get_info')
        except ConnectionError as e:
            raise e

    def get_block(self, block_num_or_id):
        try:
            body = json.dumps({'block_num_or_id': block_num_or_id})
            return self.post('get_block', data=body)
        except ConnectionError as e:
            raise e

    def get_abi(self, account_name):
        try:
            body = json.dumps({'account_name': account_name})
            return self.post('get_abi', data=body)
        except ConnectionError as e:
            raise e

    def get_code(self, account_name):
        try:
            body = json.dumps({'account_name': account_name})
            return self.post('get_code', data=body)
        except ConnectionError as e:
            raise e

    def abi_json_to_bin(self, action_data):
        try:
            return self.post('abi_json_to_bin', data=json.dumps(action_data))
        except ConnectionError as e:
            raise e

    def abi_bin_to_json(self, bin_data):
        try:
            return requests.post('abi_bin_to_json', data=bin_data)
        except ConnectionError as e:
            raise e

    def get_raw_code_and_abi(self, account_name):
        try:
            body = json.dumps({'account_name': account_name})
            return self.post('get_raw_code_and_abi', data=body)
        except ConnectionError as e:
            raise e

    def get_account(self, account_name):
        try:
            body = json.dumps({'account_name': account_name})
            return self.post('get_account', data=body)
        except ConnectionError as e:
            raise e

    def get_table_rows(self, code, scope, table, output_json=True, limit=1000, lower_bound=0, upper_bound=-1):
        try:
            body = json.dumps({'code': code, 'scope': scope, 'table': table, 'json': output_json, 'limit': limit,
                               'lower_bound': lower_bound,
                               'upper_bound': upper_bound})
            return self.post('get_table_rows', data=body)
        except ConnectionError as e:
            raise e

    def get_producers(self, limit=1000, lower_bound='', output_json=True):
        try:
            body = json.dumps({'limit': limit, 'lower_bound': lower_bound, 'json': output_json})
            return self.post('get_producers', data=body)
        except ConnectionError as e:
            raise e

    def get_required_keys(self, transaction, available_keys):
        try:
            body = json.dumps({'transaction': todict(transaction), 'available_keys': available_keys})
            return self.post('get_required_keys', data=body)
        except ConnectionError as e:
            raise e

    def push_transaction(self, transaction):
        try:
            body = json.dumps(
                {'transaction': transaction, 'signatures': transaction['signatures'], 'compression': 'none'})
            return self.post('push_transaction', data=body)
        except ConnectionError as e:
            raise e
