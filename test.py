from telospy.models import *
from telospy.api import API
from pprint import pprint
from telospy.util import to_dict
from binascii import hexlify, unhexlify
import json

if __name__ == '__main__':
    api = API('http://127.0.0.1:8888/', 'http://127.0.0.1:8999', 'v1')

    # Experiments for RPC API `setcode` endpoint

    code_file = open('/Users/hotmdev4/Desktop/telos/build/contracts/token.registry/sample.registry.wasm', 'rb')
    abi_file = open('/Users/hotmdev4/Desktop/telos/build/contracts/token.registry/sample.registry.abi', 'rb')

    abi_obj = hexlify(abi_file.read())
    code_obj = hexlify(code_file.read())
    print('abi_data: {}'.format(abi_obj))
    print('code_data: {}'.format(code_obj))

    abi_ser = b'\x0eeosio::abi/1.0\x00\n\x07setting\x00\x05\x06issuer\x04name\nmax_supply\x05asset\x06supply\x05asset\x04name\x06string\x0eis_initialized\x04bool\x07balance\x00\x02\x05owner\x04name\x06tokens\x05asset\tallotment\x00\x03\trecipient\x04name\x05owner\x04name\x06tokens\x05asset\x04mint\x00\x02\trecipient\x04name\x06tokens\x05asset\x08transfer\x00\x03\x05owner\x04name\trecipient\x04name\x06tokens\x05asset\x05allot\x00\x03\x05owner\x04name\trecipient\x04name\x06tokens\x05asset\x07reclaim\x00\x03\x05owner\x04name\trecipient\x04name\x06tokens\x05asset\x0ctransferfrom\x00\x03\x05owner\x04name\trecipient\x04name\x06tokens\x05asset\x0ccreatewallet\x00\x01\x05owner\x04name\x0cdeletewallet\x00\x01\x05owner\x04name\x07\x00\x00\x00\x00\x00\x90\xa7\x93\x04mint\x00\x00\x00\x00W-<\xcd\xcd\x08transfer\x00\x00\x00\x00\x00\x80Lc4\x05allot\x00\x00\x00\x00@:\x13\x91\xba\x07reclaim\x00 \xe9]W-<\xcd\xcd\x0ctransferfrom\x00\x90U\x8c\x86\xabl\xd4E\x0ccreatewallet\x00\x90U\x8c\x86\xab\xac\xa2J\x0cdeletewallet\x00\x03\x00\x00\x00\x98M\x97\xb3\xc2\x03i64\x01\x06issuer\x01\x04name\x07setting\x00\x00\x00X\xa1i\xa29\x03i64\x01\x05owner\x01\x04name\x07balance\x00\x00\xceS\xc9Lc4\x03i64\x01\trecipient\x01\x04name\tallotment\x00\x00\x00'
    print(hexlify(abi_ser))

    # abi_bytes = '0e656f73696f3a3a6162692f312e30000a0773657474696e67000506697373756572046e616d650a6d61785f737570706c7905617373657406737570706c79056173736574046e616d6506737472696e670e69735f696e697469616c697a656404626f6f6c0762616c616e63650002056f776e6572046e616d6506746f6b656e7305617373657409616c6c6f746d656e74000309726563697069656e74046e616d65056f776e6572046e616d6506746f6b656e73056173736574046d696e74000209726563697069656e74046e616d6506746f6b656e73056173736574087472616e736665720003056f776e6572046e616d6509726563697069656e74046e616d6506746f6b656e7305617373657405616c6c6f740003056f776e6572046e616d6509726563697069656e74046e616d6506746f6b656e73056173736574077265636c61696d0003056f776e6572046e616d6509726563697069656e74046e616d6506746f6b656e730561737365740c7472616e7366657266726f6d0003056f776e6572046e616d6509726563697069656e74046e616d6506746f6b656e730561737365740c63726561746577616c6c65740001056f776e6572046e616d650c64656c65746577616c6c65740001056f776e6572046e616d6507000000000090a793046d696e7400000000572d3ccdcd087472616e736665720000000000804c633405616c6c6f7400000000403a1391ba077265636c61696d0020e95d572d3ccdcd0c7472616e7366657266726f6d0090558c86ab6cd4450c63726561746577616c6c65740090558c86abaca24a0c64656c65746577616c6c65740003000000984d97b3c203693634010669737375657201046e616d650773657474696e6700000058a169a2390369363401056f776e657201046e616d650762616c616e63650000ce53c94c6334036936340109726563697069656e7401046e616d6509616c6c6f746d656e74000000'
    # print('dehex_abi: {}'.format(unhexlify(abi_bytes)))
