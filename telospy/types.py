

# TODO: Create all of the EOSIO types using numpy and either colander/marshmallow

# EOSIO Types

# block_time_stamp


# Names
# see eos/libraries/chain/include/eosio/chain/name.hpp?L#21

# Name : uint64 bit encoded name type or string
# AccountName : Name Type
# ScopeName : Name Type
# PermissionName : Name Type
# ActionName : Name Type
# TableName : Name Type

# Native Structs

# Authority Struct : {'threshold': uint32, 'keys': [KeyWeight], 'accounts': [AccountWeight], 'waits': [WaitWeight]}
# KeyWeight Struct : {'key': PublicKey, 'weight': uint16}
# WaitWeight Struct : {'wait_sec': uint32, 'weight': uint16}
# Asset Struct : {'amt': int64, 'symbol': Symbol}
# Symbol Struct : {'precision': ubyte, 'name': string} - uint64 encoded precision and name

# ABI.ABI Structs

# ABI Struct : {'version': string, 'types': [ABIType], 'structs': [StructType],
#                   'actions': [ActionType], 'tables': [TableType], 'clauses': [ClauseType],
#                   'error_messages': [ABIErrorMessageType], 'abi_extensions': [ExtensionsType]}

# ABIType : {'new_type_name': string, 'type': type}

# StructType : {'name': string, 'base': string, 'fields': [FieldType]}

# FieldType : {'name': string, 'type': string}

# ActionType : {'name': ActionName, 'type': string, 'ricardian_contract': string}

# TableDef : {'name': TableName, 'index_type': string, 'key_names': [string], 'key_types': [string], 'type': string}

# ClauseType : {'id': string, 'body': string}

# ABIErrorMessageType : {'error_code': uint64, 'error_msg': string}


