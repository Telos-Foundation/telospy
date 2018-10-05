# Names
# see eos/libraries/chain/include/eosio/chain/name.hpp?L#21


class Name(object):

    def __init__(self, name='', value=0):
        self._value = value
        self._name = name

    @property
    def name(self):
        if self._name is not '':
            return self._name
        elif self._value is not 0:
            return Name.name_to_string(self._value)
        raise ValueError('Name object was not initialized with a value or name')

    @property
    def value(self):
        if self._value is not 0:
            return self._value
        elif self._name is not '':
            return Name.string_to_name(self._name)
        raise ValueError('Name object was not initialized with a value or name')

    @staticmethod
    def string_to_name(name_string):
        name = 0
        for i in range(0, len(name_string)):
            name |= (Name.char_to_symbol(name_string[i]) & 0x1f) << (64 - 5 * (i + 1))
        if i == 12:
            name |= Name.char_to_symbol(name_string[12]) & 0x0F;

        return name

    @staticmethod
    def name_to_string(name_value):
        map = ".12345abcdefghijklmnopqrstuvwxyz";
        name_list = ['.'] * 13

        tmp = name_value

        for i in range(0, 13):
            c = map[tmp & (0x0f if i == 0 else 0x1f)] # (i == 0 ? 0x0f : 0x1f)
            name_list[12-i] = c
            tmp >>= (4 if i == 0 else 5)

        for char in reversed(name_list):
            curr = len(name_list) - 1
            if char == '.':
                del name_list[curr]
                curr -= 1
            else:
                break

        name_string = ''
        for c in name_list:
            name_string += c

        return name_string

    @staticmethod
    def char_to_symbol(c):
        c = ord(c)
        if c >= ord('a') and c <= ord('z'):
            return (c - ord('a')) + 6
        if c >= ord('1') and c <= ord('5'):
            return (c - ord('1')) + 1
        return 0


class AccountName(Name):
    pass


class PermissionName(Name):
    pass


class ScopeName(Name):
    pass


class ActionName(Name):
    pass


class TableName(Name):
    pass


# EOSIO Types
# Native Structs

class BlockTimeStamp(object):
    pass


class Authority(object):
    pass


class KeyWeight(object):
    pass


class AccountWeight(object):
    pass


class WaitWeight(object):
    pass


class Asset(object):
    pass


class Symbol(object):

    def __init__(self, name, precision):
        self.name = name
        self.precision = precision

    @staticmethod
    def string_to_symbol(string, precision):
        result = 0;
        length = len(string)
        for i in range(0, length):
            c = ord(string[i])
            if c < ord('A') or c > ord('Z'):
                raise ValueError('symbol name contains out of range characters: {}'.format(c))
            else:
                result |= (int(c) << (8*(1+i)))

        result |= int(precision)
        return result

    @staticmethod
    def is_valid(sym):
        pass
        # sym >>= 8
        # for i in range(0, 7):
        #     c = ord(sym & 0xff)
        #     if not (ord('A') <= c and c <= ord('z')):
        #         return False
        #     if not (sym& 0xff):

# ABI TYPEs
# TODO: Call super constructor to remove boiler plate


class ABI(object):

    def __init__(self, *args, **kwargs):
        self.version = ''
        self.types = []
        self.structs = []
        self.actions = []
        self.tables = []
        self.clauses = []
        self.error_messages = []
        self.abi_extensions = []

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class ABIType(object):

    def __init__(self, *args, **kwargs):
        self.new_type_name = ''
        self.type = ''

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Struct(object):

    def __init__(self, *args, **kwargs):
        self.name = ''
        self.base = ''
        self.fields = []

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Field(object):

    def __init__(self, *args, **kwargs):
        self.name = ''
        self.type = ''

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Action(object):

    def __init__(self, *args, **kwargs):
        self.name = ''
        self.type = ''
        self.ricardian_contract = ''

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Table(object):

    def __init__(self, *args, **kwargs):
        self.name = ''
        self.index_type = ''
        self.key_names = []
        self.key_types = []
        self.type = []

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Clause(object):

    def __init__(self, *args, **kwargs):
        self.id = ''
        self.body = ''

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class ABIErrorMessage(object):

    def __init__(self, *args, **kwargs):
        self.error_code = ''
        self.error_msg = ''

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


from binascii import hexlify, unhexlify

if __name__ == '__main__':
    value = 12531434851120166560
    name = 'prodnameyyve'
    name_string = Name.name_to_string(value)
    name_value = Name.string_to_name(name)
    assert name_value == 12531434851120166560, 'name_value {} must equal input name {}'.format(name_value, value)
    assert name_string == name, 'name_string {} must equal input name {}'.format(name_string, name)
    print('value {} == name {}'.format(value, name))

    obj = Name(value=value)
    assert obj.name == name, 'Name.name {} must equal input name {}'.format(obj.name, name)
    assert obj.value == value, 'Name.value {} must equal input value {}'.format(obj.value, value)

    print(hexlify(b'12531434851120166560'))


