from telospy.models import *
from telospy.api import API
from telospy.serialize import SerialBuffer
from telospy.serialize import *
from telospy.types import *
from binascii import hexlify, unhexlify
from datetime import datetime

if __name__ == '__main__':
    api = API('http://127.0.0.1:8888/', 'http://127.0.0.1:8999', 'v1')

    ser = SerialBuffer()

    # value = 4294967295
    # print("{0:b}".format(value))
    # ser.push_u_int_32(value)
    # result = ser.get_u_int_32()
    # assert value == result, "returned value does not equal value"
    # print("value: {} == result: {}".format(value, result))
    #
    # value2 = 18446744073709551615
    # print("{0:b}".format(value2))
    # ser.push_u_int_64(value2)
    # result2 = ser.get_u_int_64()
    # assert value2 == result2, "returned value does not equal value"
    # print("value2: {} == result2: {}".format(value2, result2))

    # ser.push_name(Name(name='eosio'))
    # ser.push_name(Name(name='testtesttest'))
    # ser.push_asset("1000.0000 TLOS")
    # ser.push_string("test123")
    #
    # theirs = b'0000000000ea305590b1ca19ab9cb1ca809698000000000004544c4f530000000774657374313233'
    # print("theirs: {}".format(theirs))
    #
    # mine = hexlify(ser.array)
    #
    # print("  mine: {}".format(mine))

    date1 = str(datetime.utcnow())
    block_time_stamp = date_to_block_time_stamp(date1)
    date2 = block_time_stamp_to_date(block_time_stamp)
    print(date1)
    print(date2)

    # 591984382










