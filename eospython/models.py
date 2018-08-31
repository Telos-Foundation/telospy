from datetime import datetime
from datetime import timedelta
from . import api
import logging

__all__ = ['Transaction', 'AccountName', 'ActionData', 'Action', 'Authority']


class Transaction:
    logger = logging.getLogger(__name__)

    def __init__(self, *initial_data, **kwargs):
        """Transaction - The Python Object representation of an EOSIO Transaction"""
        self.expiration = (datetime.utcnow() + timedelta(minutes=2)).isoformat()
        self.ref_block_num = 0
        self.ref_block_prefix = 0
        self.max_net_usage_words = 0
        self.max_cpu_usage_ms = 0
        self.delay_sec = 0
        self.context_free_actions = []
        self.context_free_data = []
        self.actions = []
        self.signatures = []

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        if self.ref_block_num == 0:
            self.ref_block_num = self.get_ref_block_num()

        if self.ref_block_prefix == 0:
            self.ref_block_prefix = self.get_ref_block_prefix(self.ref_block_num)

    def add_action(self, action):
        if not self.actions:
            self.actions = []
        self.actions.append(action)

    def get_ref_block_num(self):
        r = api.chain_api.get_info()
        if r.status_code == 200:
            return r.json()['head_block_num']
        else:
            Transaction.logger.error('get_ref_block_num failed')

    def get_ref_block_prefix(self, block_num):
        r = api.chain_api.get_block(block_num)
        if r.status_code == 200:
            return r.json()['ref_block_prefix']
        else:
            Transaction.logger.error('get_ref_block_prefix failed')

    def send(self):
        """Send transaction"""


class AccountName:

    def __init__(self, name):
        """Python object representation of an EOSIO account_name"""
        self.account_name = name

    def exists(self):
        """Checks to see if an account exists"""
        r = api.chain_api.get_account(self.account_name)
        if r:
            return r['account_name'] is self.account_name
        return False


class Authority:

    def __init__(self, actor, permission):
        """Authority is the account_name and permission name used to authorize an action"""
        self.actor = actor
        self.permission = permission

    def exists(self):
        r = api.chain_api.get_account(self.account_name)
        if r:
            for permission in r['permissions']:
                if permission is self.permission:
                    return True
        return False


class Action:

    def __init__(self, account, action_name, data):
        """Action is used in pushing transactions to the RPC API"""
        self.account = account  # NOTE: code, is the account_name the contract is set on.
        self.name = action_name
        self.authorization = []  # NOTE: Authorization is the permission_level used for the action
        self.data = data  # NOTE: Data is the binargs received from abi_json_to_bin RPC

    def add_authorization(self, authority):
        # TODO: Validate given authority
        self.authorization.append(authority)

    # action.validate()


class ActionData:
    logger = logging.getLogger(__name__)

    def __init__(self, code, action, args):
        """ActionData is used to get bin data from the RPC API"""
        self.code = code
        self.action = action
        self.args = args

    def get_action(self):
        r = api.chain_api.abi_json_to_bin(self.__dict__)
        ActionData.logger.debug('Attempting to retrieve abi binary arguments')
        if r.status_code == 200:
            j = r.json()
            ActionData.logger.debug('Success: %s', j['binargs'])
            return Action(self.code, self.action, j['binargs'])
        else:
            ActionData.logger.error('Was unable to parse binargs from abi_json_to_bin')
