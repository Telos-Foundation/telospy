from eospython.models import *
from eospython.api import API
from pprint import pprint

if __name__ == '__main__':
    api = API('http://127.0.0.1:8888/', 'http://127.0.0.1:8999', 'v1')

    action_data = ActionData('eosio.token', 'transfer',
                              {'from': 'eosio', 'to': 'goodblockio1', 'quantity': '1000.0000 TLOS',
                               'memo': 'for testing or whatever'})
    authority = Authority('eosio', 'active')
    receipt = api.send_transaction(action_data, authority)

    pprint(receipt)




