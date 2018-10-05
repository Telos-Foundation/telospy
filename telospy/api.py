import logging
import requests
from urllib import parse
from .models import *
from .exceptions import *
from .util import to_dict

__all__ = ['WalletAPI', 'ChainAPI', 'API']


class API:

    def __init__(self, url, wallet_url='http://127.0.0.1:8999', version='v1'):
        self._wallet_api = None
        self._chain_api = None
        self.logger = logging.getLogger(__name__)

        assert isinstance(url, str), "`url` is not a string"
        self.logger.debug('Configuring chain_api instance')
        self._chain_api = ChainAPI(url, version)

        assert isinstance(wallet_url, str), "`wallet_url` is not a string"
        self.logger.debug('Configuring wallet_api instance')
        self._wallet_api = WalletAPI(wallet_url, version)

    @property
    def chain(self):
        if not self._chain_api:
            self.logger.error(msg='_chain_api is None')
            raise APINotConfigured('Chain API has not yet been configured. api.configure_chain_api(url)')
        self.logger.debug('returning ChainAPI instance')
        return self._chain_api

    @property
    def wallet(self):
        if not self._wallet_api:
            self.logger.error(msg='_wallet_api is None')
            raise APINotConfigured('Wallet API has not yet been configured. api.configure_wallet_api()')
        self.logger.debug('returning WalletAPI instance')
        return self._wallet_api

    def get_chain_lib_info(self):
        """Gets required chain information for trx"""
        chain_info = self.chain.get_info()
        lib_info = self.chain.get_block(chain_info['last_irreversible_block_num'])
        return chain_info, lib_info

    def get_account_info(self, account_name):
        try:
            return self.chain.get_account(account_name)
        except ChainAPIException:  # NOTE: This exception is too specific
            raise AccountDoesNotExistException('The account does not exist on this chain')

    def does_action_exist(self, account_name, action_name, account_info={}):
        assert isinstance(account_name, str), "`account_name` must be a String"
        if isinstance(account_info, dict) and 'account_name' in account_info:
            assert account_name == account_info['account_name'], \
                'the `account_information given does not match the provided account_name`'
            account_name = account_info['account_name']
        abi_info = self.chain.get_abi(account_name)
        if 'abi' not in abi_info:
            raise AccountABIDoesNotExistException('account_name `%s` does not have an ABI' % account_name)

        if 'actions' in abi_info['abi']:
            for action in abi_info['abi']['actions']:
                if action['name'].lower() == action_name.lower():
                    return True
        return False

    def does_permission_exist(self, account_info, permission_name):
        if 'permissions' in account_info:
            for permission in account_info['permissions']:
                if permission['perm_name'].lower() == permission_name.lower():
                    return True
        return False

    def get_bin_data(self, action):
        return self.chain.abi_json_to_bin(action)['binargs']

    ####################
    # Basic Chain Commands
    ####################

    # TODO: refactor to be more verbose. Where owner and active can be either keys or account permissions
    # TODO: refactor this use new Authority model instead of dictionaries
    def create_account(self, creator, account_name, owner, active='', stake_net='1000.0000 TLOS',
                       stake_cpu='1000.0000 TLOS',
                       ram_kb=1024, permission='active', transfer=True):
        try:
            self.get_account_info(account_name)
            raise AccountAlreadyExistsException('The account already exists on this chain')
        except AccountDoesNotExistException:
            pass

        owner_auth = {"threshold": "1", "keys": [{"key": owner, "weight": 1}], 'accounts': [], "waits": []}
        if active is '':
            active_auth = owner_auth
        else:
            active_auth = {"threshold": "1", "keys": [{"key": owner, "weight": 1}], 'accounts': [], "waits": []}

        create_action = Action('eosio', 'newaccount',
                               {'creator': creator, 'name': account_name, 'owner': owner_auth, 'active': active_auth},
                               Permission(creator, permission))
        buy_ram_action = Action('eosio', 'buyrambytes',
                                {'payer': creator, 'receiver': account_name, 'bytes': ram_kb * 1024},
                                Permission(creator, permission))
        delegate_bw_action = Action('eosio', 'delegatebw',
                                    {'from': creator, 'receiver': account_name, 'stake_net_quantity': stake_net,
                                     'stake_cpu_quantity': stake_cpu, 'transfer': transfer},
                                    Permission(creator, permission))

        return self.send_transaction(actions=[create_action, buy_ram_action, delegate_bw_action])

    def set_contract(self):
        raise NotImplementedError('set_contract is currently not implemented')

    def transfer(self, sender, recipient, amount, memo):
        args = {'from': sender, 'to': recipient, 'quantity': amount, 'memo': memo}
        permission = Permission(sender, 'active')
        transfer_action = Action(account='eosio.token', action_name='transfer', args=args, authorizations=permission)
        return self.send_transaction(actions=[transfer_action])

    def update_auth(self):
        raise NotImplementedError('update_auth is not currently implemented')

    def send_transaction(self, actions):
        """Send a transaction with a single action in it."""
        if isinstance(actions, Action):
            actions = [actions]
        elif not isinstance(actions, list):
            raise AssertionError('actions must be a list of Actions or a single Action')

        chain_info, lib_info = self.get_chain_lib_info()

        for action in actions:
            for auth in action.authorization:
                auth_info = self.get_account_info(auth.actor)
                if not self.does_permission_exist(auth_info, auth.permission):
                    raise PermissionDoesNotExistException('account_name `%s` does not have permission `%s`'
                                                          % (auth.actor, auth.permission))
            code_info = self.get_account_info(action.account)  # NOTE: this method will raise an exception if it fails

            if not self.does_action_exist(action.code, action.name, code_info):
                raise ActionDoesNotExistException('`%s` ABI does not contain an action named `%s`'
                                                  % (action.code, action.name))
            action.data = self.get_bin_data(to_dict(action))
            self.logger.debug('action bin data: {}'.format(action.data))

        trx = Transaction(actions=actions)
        trx.set_ref_data(chain_info, lib_info)

        key_for_signing = self.chain.get_required_keys(trx, self.wallet.get_public_keys())

        signed_transaction = self.wallet.sign_transaction(trx, key_for_signing['required_keys'], chain_info['chain_id'])
        return self.chain.push_transaction(signed_transaction)


class APIBase:

    def __init__(self, headers, base_url):
        """Base API class"""
        self.base_headers = headers
        self.base_url = base_url
        self.params = {}
        self.logger = logging.getLogger(__name__)

    def post(self, endpoint, data=None, params={}, headers={}, json={}):
        self.logger.debug(json)
        m_headers = {**self.base_headers, **headers}
        m_params = {**self.params, **params}
        return requests.post(url=parse.urljoin(self.base_url, endpoint), data=data, headers=m_headers, params=m_params,
                             json=json)


class WalletAPI(APIBase):

    def __init__(self, base_url, version):
        """Wallet API for communicating with EOSIO wallet RPCs."""
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        APIBase.__init__(self, headers, parse.urljoin(base_url, '/%s/wallet/' % version))

        self.logger.debug('Constructing %s', __name__)

    # TODO: to improve exception handling, it might be best to create an error handler function
    # that throws more specific API exceptions depending on the API
    def post(self, endpoint, data=None, params={}, headers={}, json={}):
        response = super(WalletAPI, self).post(endpoint, data, params, headers, json)
        if response.status_code >= 400:
            raise WalletAPIException(response=response)
        return response.json()

    def create(self, name):
        return self.post('create', data="\"%s\"" % name)

    def unlock(self, password, name='default'):
        body = [name, password]
        return self.post('unlock', json=body)

    def lock(self, name='default'):
        return self.post('lock', data="\"%s\"" % name)

    def list_wallets(self):
        return self.post('list_wallets')

    def list_keys(self, password, name='default'):
        body = [name, password]
        return self.post('list_keys', json=body)

    def get_public_keys(self):
        return self.post('get_public_keys')

    def create_key(self, key_type="K1", name="default"):
        body = [name, key_type]
        return self.post('create_key', json=body)

    def import_key(self, private_key, name='default'):
        body = [name, private_key]
        return self.post('import_key', json=body)

    def set_timeout(self, time_out):
        return self.post('set_timeout', data=str(time_out))

    def sign_transaction(self, transaction, keys, chain_id=""):
        body = [to_dict(transaction), keys, chain_id]
        return self.post('sign_transaction', json=body)


class ChainAPI(APIBase):

    def __init__(self, base_url, version):
        """Chain API class for communicating with EOSIO based chain RPCs."""
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        APIBase.__init__(self, headers, parse.urljoin(base_url, '/%s/chain/' % version))

    # TODO: to improve exception handling, it might be best to create an error handler function
    # that throws more specific API exceptions depending on the API
    def post(self, endpoint, data=None, params={}, headers={}, json={}):
        response = super(ChainAPI, self).post(endpoint, data, params, headers, json)
        if response.status_code >= 400:
            raise ChainAPIException(response=response)
        return response.json()

    def get_currency_balance(self, account, code='eosio.token', symbol='TLOS'):
        body = {'code': code, 'account': account, 'symbol': symbol}
        return self.post('get_currency_balance', json=body)

    def get_currency_stats(self, account, symbol='TLOS'):
        body = {'code': 'eosio.token', 'account': account, 'symbol': symbol}
        return self.post('get_currency_stats', json=body)

    def get_block_header_state(self, block_num):
        body = {'block_num_or_id': block_num}
        return self.post('get_block_header_state', json=body)

    def get_info(self):
        return self.post('get_info')

    def get_block(self, block_num_or_id):
        body = {'block_num_or_id': block_num_or_id}
        return self.post('get_block', json=body)

    def get_abi(self, account_name):
        body = {'account_name': account_name}
        return self.post('get_abi', json=body)

    def set_abi(self, account_name, abi_bin):
        body = {'account': account_name, 'abi': abi_bin}
        return self.post('set_abi', json=body)

    def get_code(self, account_name):
        body = {'account_name': account_name}
        return self.post('get_code', json=body)

    def set_code(self, account, code, vmtype=0, vmversion=0):
        body = {'account': account, 'vmtype': vmtype, 'vmversion': vmversion, 'code': code}
        return self.post('set_code', json=body)

    def abi_json_to_bin(self, action):
        return self.post('abi_json_to_bin', json=action)

    def abi_bin_to_json(self, bin_data):
        return self.post('abi_bin_to_json', json=bin_data)

    def get_raw_code_and_abi(self, account_name):
        body = {'account_name': account_name}
        return self.post('get_raw_code_and_abi', json=body)

    def get_account(self, account_name):
        body = {'account_name': account_name}
        return self.post('get_account', json=body)

    def get_table_rows(self, code, scope, table, output_json=True, limit=1000, lower_bound=0, upper_bound=-1):
        body = {'code': code, 'scope': scope, 'table': table, 'json': output_json, 'limit': limit,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound}
        return self.post('get_table_rows', json=body)

    def get_producers(self, limit=1000, lower_bound='', output_json=True):
        body = {'limit': limit, 'lower_bound': lower_bound, 'json': output_json}
        return self.post('get_producers', json=body)

    def get_required_keys(self, transaction, available_keys):
        body = {'transaction': to_dict(transaction), 'available_keys': available_keys}
        return self.post('get_required_keys', json=body)

    def push_transaction(self, transaction):
        body = {'transaction': transaction, 'signatures': transaction['signatures'], 'compression': 'none'}
        return self.post('push_transaction', json=body)
