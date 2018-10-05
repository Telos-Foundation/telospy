from math import ceil
from .types import *
from datetime import datetime
from dateutil.parser import parse as date_parse, isoparse as date_isoparse
from time import time


# TODO: Type checking


class SerialBuffer(object):

    def __init__(self):
        self.length = 0
        self.array = bytearray(0)
        self.r_pos = 0

    def reset_read(self):
        self.r_pos = 0

    def print(self):
        for b in self.array:
            print(b)

    def reserve(self, size):
        if self.length + size <= len(self.array):
            return
        l = len(self.array)
        while self.length + size > l:
            l = ceil(l * 1.5);

        new_array = bytearray(l)
        self.array = self.array + new_array

    # BYTE MANAGEMENT

    def push_bytes(self, bytes_array):
        self.array = self.array + bytes_array
        self.length += len(bytes_array)

    def push_byte(self, *args):
        new_array = bytearray()
        for v in args:
            new_array.append(v)
        self.push_bytes(new_array)

    def get_byte(self):
        if self.r_pos < self.length:
            byte = self.array[self.r_pos]
            self.r_pos += 1
            return byte
        else:
            raise IndexError('you have attempted to get a byte out of range of this array')

    def get_bytes(self, length):
        if self.r_pos + length > self.length:
            raise ValueError('length given for get_bytes exceeds length of buffer')
        result = self.array[self.r_pos:self.r_pos + length]
        self.r_pos = self.r_pos + length
        return result

    # Unsigned Integers

    def push_int(self, val, size):
        for i in range(0, size):
            self.push_byte((val >> (i * 8)) & 0xff)

    def get_int(self, size):
        v = 0
        for i in range(0, size):
            v |= self.get_byte() << (i * 8)
        return v

    def push_u_int_16(self, val):
        self.push_int(val, 2)

    def get_u_int_16(self):
        return self.get_int(2)

    def push_u_int_32(self, val):
        self.push_int(val, 4)

    def get_u_int_32(self):
        return self.get_int(4)

    def push_u_int_64(self, val):
        self.push_int(val, 8)

    def get_u_int_64(self):
        return self.get_int(8)

    def push_u_int_128(self, val):
        self.push_int(val, 16)

    def get_u_int_128(self):
        return self.get_int(16)

    # SIGNED INTEGERS
    # TODO: make signed 16, 64, 128 types
    def push_int_16(self, val):
        self.push_u_int_16((val << 1) ^ (val >> 15))

    def get_int_16(self):
        val = self.get_u_int_16()
        if val & 1:
            return ((~val) >> 1) | 0x8000
        else:
            return val >> 1

    def push_int_32(self, val):
        self.push_u_int_32((val << 1) ^ (val >> 31))

    def get_int_32(self):
        val = self.get_u_int_32()
        if val & 1:
            return ((~val) >> 1) | 0x8000_0000
        else:
            return val >> 1

    def push_int_64(self, val):
        self.push_u_int_64((val << 1) ^ (val >> 63))

    def get_int_64(self):
        val = self.get_u_int_64()
        if val & 1:
            return ((~val) >> 1) | 0x8000_0000_0000
        else:
            return val >> 1

    def push_int_128(self, val):
        self.push_u_int_128((val << 1) ^ (val >> 127))

    def get_int_128(self):
        val = self.get_u_int_128()
        if val & 1:
            return ((~val) >> 1) | 0x8000_0000_0000_0000_0000_0000_0000_0000
        else:
            return val >> 1

    # FLOATING POINT

    def push_float_32(self, val):
        pass

    def get_float_32(self):
        pass

    def push_float_64(self, val):
        pass

    def get_float_64(self):
        pass

    def push_float_128(self, val):
        pass

    def get_float_128(self):
        pass

    # CHAIN TYPES

    def push_string(self, val):
        char_count = len(val)
        self.push_byte(char_count)
        self.push_bytes(val.encode())

    def get_string(self, encoding='utf-8'):
        char_count = self.get_u_int_32()
        result = self.get_bytes(char_count)
        return result.decode(encoding)

    def push_name(self, val):
        self.push_u_int_64(val.value)

    def get_name(self):
        return Name(value=self.get_u_int_64())

    def push_symbol(self, val):
        self.push_u_int_64(Symbol.string_to_symbol(val.name, val.precision))

    def get_symbol(self, encoding='utf-8'):
        precision = self.get_byte()
        a = self.get_bytes(7)
        name_result = []
        for c in a:
            if c >= ord('A') and c <= ord('Z'):
                name_result.append(c)

        return Symbol(bytearray(name_result).decode(encoding), precision)

    def push_asset(self, val): # TODO: Refactor to reduce number of in-range checks
        assert isinstance(val, str), "input must be of type string"
        input = val.strip()
        amount = ''
        precision = 0
        i = 0

        if input[0] is '-':
            amount += "-"
            i += 1

        is_digit = False

        while i < len(input) and ord(input[i]) >= ord("0") and ord(input[i]) <= ord('9'):
            is_digit = True
            amount += input[i]
            i += 1

        assert is_digit, "asset must contain a numeric value"

        if input[i] is '.':
            i += 1
            while i < len(input) and ord(input[i]) >= ord("0") and ord(input[i]) <= ord('9'):
                amount += input[i]
                precision += 1
                i += 1

        name = input[i:len(input)].strip()
        self.push_bytes(signed_decimal_to_binary(amount, 8))
        self.push_symbol(Symbol(name=name, precision=precision))

    def get_asset(self): # TODO: Finish this method with proper algo
        amount = self.get_bytes(8)
        sym = self.get_symbol()
        s = signed_binary_to_decimal(amount, sym.precision + 1)
        if sym.precision:
            s = s[0:len(s)-sym.precision] + "." + s[len(s) - sym.precision:len(s) + 1]
        return "{} {}".format(s, sym.name)

    # TODO: LATER

    def push_pub_key(self, val):
        pass

    def get_pub_key(self):
        pass

    def push_priv_key(self, val):
        pass

    def get_priv_key(self):
        pass

    def push_signature(self, val):
        pass

    def get_signature(self):
        pass

# TODO: Create a recursive crawler that serializes inputs based on target action's ABI struct


def decimal_to_binary(input, size):
    result = bytearray(size)
    for i in range(0, len(input)):
        curr = ord(input[i])
        if curr < ord('0') or curr > ord('9'):
            raise ValueError('input decimal is malformed')
        carry = curr - ord('0')
        for j in range(0, size):
            x = result[j] * 10 + carry
            result[j] = x & 0xff
            carry = x >> 8
        if carry:
            raise ValueError('number is out of range')
    return result


def binary_to_decimal(input, min_digits=1):
    result = [ord("0") for i in range(min_digits)]
    for c in input[::-1]:
        carry = c
        for j in range(0, len(result)):
            x = ((result[j] - ord("0")) << 8) + carry
            result[j] = ord("0") + x % 10
            carry = int((x / 10)) | 0
        while carry:
            result.append(ord("0") + carry % 10)
            carry = int((carry / 10)) | 0
    output = ''
    for c in reversed(result):
        output += chr(c)
    return output


def signed_binary_to_decimal(input, min_digits=1):
    if is_negative(input):
        x = input.copy()
        negate(x)
        return '-' + binary_to_decimal(x, min_digits)
    return binary_to_decimal(input, min_digits)


def signed_decimal_to_binary(input, size):
    negative = input[0] is '-'
    if negative:
        input = input[1:len(input)]
    result = decimal_to_binary(input, size)
    if negative:
        negate(result)
        if not is_negative(result):
            raise ValueError('number is out of range')
    elif is_negative(result):
        raise ValueError('number is out of range')
    return result


def negate(val):
    carry = 1
    for i in range(0, len(val)):
        x = (~val[i] & 0xff) + carry
        val[i] = x
        carry = x >> 8


def is_negative(val):
    return (val[len(val) - 1] & 0x80) is not 0


# Date functions

epoch_2000 = 946684800000
epoch_2000_sec = epoch_2000 / 1000


def date_check(date):
    return date_isoparse(date)

# TO/FROM time_point
# Remove timezone awareness - AKA ZULU TIME
# time_points are in us or ms


def date_to_time_point(date):
    return round((date_check(date) - datetime.utcfromtimestamp(0)).total_seconds() * 1000000)


def time_point_to_date(us):
    return datetime.utcfromtimestamp((us / 1000000))


# TO/FROM time_point_sec

def date_to_time_point_sec(date):
    return round((date_check(date) - datetime.utcfromtimestamp(0)).total_seconds())


def time_point_sec_to_date(sec):
    return datetime.utcfromtimestamp(sec)

# TO/FROM block_time_stamp


def date_to_block_time_stamp(date):
    return ((date_check(date) - datetime.utcfromtimestamp(0)).total_seconds() - epoch_2000_sec) * 500


def block_time_stamp_to_date(slot):
    slot_sec = slot / 500
    return datetime.utcfromtimestamp(slot_sec + epoch_2000_sec)
