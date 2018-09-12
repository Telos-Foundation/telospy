from eospython.models import *
from eospython.api import API
from pprint import pprint

if __name__ == '__main__':
    api = API('http://127.0.0.1:8890/', 'http://127.0.0.1:8999', 'v1')
    data = {'account': 'eosio', 'name': 'newaccount', 'code': 'eosio', 'action': 'newaccount', 'args': {'creator': 'eosio', 'name': 'craigissuper', 'owner': 'TLOS55oLsFKcv3EEcJfDK81CX7UrbL8T9zfuLZHMXoSJSXBpvX4kxd', 'active': 'TLOS55oLsFKcv3EEcJfDK81CX7UrbL8T9zfuLZHMXoSJSXBpvX4kxd'}}
    data2 = {'code': 'eosio.token', 'action': 'transfer',
             'args': {'from': 'eosio', 'to': 'goodblockio1', 'quantity': '1000.0000 TLOS',
                      'memo': 'for testing or whatever'}}
    json = api.chain.abi_json_to_bin(data)
    pprint(json)

    # action_data = ActionData('eosio.token', 'transfer',
    #                           {'from': 'eosio', 'to': 'goodblockio1', 'quantity': '1000.0000 TLOS',
    #                            'memo': 'for testing or whatever'})
    # authority = Authority('eosio', 'active')
    # receipt = api.send_transaction(action_data, authority)
    #
    # pprint(receipt)
