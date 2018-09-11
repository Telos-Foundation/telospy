from datetime import datetime
from datetime import timedelta
import logging

__all__ = ['Transaction', 'AccountName', 'ActionData', 'Action', 'Authority']

# TODO: create schemas using either marshmallow or colander


class ModelBase(object):
    """Base class for all eosPython models"""


class Asset(ModelBase):
    pass


class Transaction(ModelBase):
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

    def set_ref_data(self, chain_info, lib_info):
        if chain_info is not None:
            self.ref_block_num = chain_info['last_irreversible_block_num']
        if lib_info is not None:
            self.ref_block_prefix = lib_info['ref_block_prefix']

    def add_action(self, action):
        if not self.actions:
            self.actions = []
        self.actions.append(action)


class AccountName(ModelBase):

    def __init__(self, name):
        """Python object representation of an EOSIO account_name"""
        assert isinstance(name, str), "Argument name must be type string"
        self.account_name = name


class Authority(ModelBase):

    def __init__(self, actor, permission):
        """Authority is the account_name and permission name used to authorize an action"""
        assert isinstance(actor, str), "Argument `actor` must be type String"
        assert isinstance(permission, str), "Argument `permission` must be type String"
        self.actor = actor
        self.permission = permission


class Action(ModelBase):
    logger = logging.getLogger(__name__)

    def __init__(self, account, action_name, data):
        """Action is used in pushing transactions to the RPC API"""
        assert isinstance(account, str), "Argument account must be type String"
        assert isinstance(action_name, str), "Argument action_name must be type String"
        self.account = account  # NOTE: code, is the account_name the contract is set on.
        self.name = action_name
        self.authorization = []  # NOTE: Authorization is the permission_level used for the action
        self.data = data  # NOTE: Data is the binargs received from abi_json_to_bin RPC

    def add_authorization(self, authority):
        Action.logger.debug('Attempting to verify authority for account: %s, permission: %s' % (
            authority.actor, authority.permission))
        self.authorization.append(authority)


class ActionData(ModelBase):
    logger = logging.getLogger(__name__)

    def __init__(self, code, action, args):
        """ActionData is used to get bin data from the RPC API"""
        assert isinstance(code, str), "Argument `code` must be type `String`"
        assert isinstance(action, str), "Argument `action` must be type `String`"
        assert isinstance(args, dict), "Argument `args` must be type `list`"
        self.code = code
        self.action = action
        self.args = args

