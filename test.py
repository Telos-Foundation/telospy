from eospython.models import *
import eospython.api as api


if __name__ == '__main__':
    api.configure_chain_api('http://127.0.0.1:8888/')
    api.configure_wallet_api('http://127.0.0.1:8999/')
    action_data = ActionData('eosio.token', 'transfer',
                             {'from': 'eosio', 'to': 'goodblockio1', 'quantity': '1000.0000 TLOS',
                              'memo': 'for testing or whatever'})

    action = action_data.get_action()
    action.add_authorization(Authority('eosio', 'active'))
    trans = Transaction(actions=[action])
    public_keys = api.wallet_api.get_public_keys().json()
    print(public_keys)
    key_for_signing = api.chain_api.get_required_keys(trans, public_keys)
    print(key_for_signing.json())
    signed_transaction = api.wallet_api.sign_transaction(trans, key_for_signing.json()['required_keys'],
                                                    api.chain_api.get_info().json()['chain_id'])
    receipt = api.chain_api.push_transaction(signed_transaction.json())
    print(receipt.json())



