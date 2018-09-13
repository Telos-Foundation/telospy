from telospy.api import API
from telospy.models import Action
from telospy.models import Permission
from telospy.exceptions import AccountAlreadyExistsException

# This example assumes that there is a node running locally on the machine
# It also assumes that the chain is a telos chain, but telospy works on either telos or eos

api = API('http://127.0.0.1:8888', 'http://127.0.0.1:8999', 'v1')

try:
    api.create_account('eosio', 'goodblockio1', 'TLOS8BLqdVB2Lk4qppxrUkA3xGrgqbgbiBLM5iey7X5t1LbDYkG2yA')
except AccountAlreadyExistsException:
    pass

args = {'from': 'eosio', 'to': 'goodblockio1', 'quantity': '1000.0000 TLOS', 'memo': 'Sent from telospy!'}
permission = Permission('eosio', 'active')
transfer_action = Action(account='eosio.token', action_name='transfer', args=args, authorizations=permission)

receipt = api.send_transaction(transfer_action)

print(receipt)