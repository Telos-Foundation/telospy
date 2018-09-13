"""
eosPython exceptions
"""
from requests.exceptions import RequestException

__all__ = ['APIResponseException', 'WalletAPIException', 'ChainAPIException', 'APINotConfigured', 'ModelException',
           'PermissionDoesNotExistException', 'AccountDoesNotExistException', 'AccountABIDoesNotExistException',
           'ActionDoesNotExistException', 'AccountAlreadyExistsException']

# TODO: write handlers, that are used by the API(s) to raise verbose exceptions based on
# information returned by the RPC API


def wallet_exception_raiser():
    pass


def chain_exception_raiser():
    pass


################
# API EXCEPTIONS
################


class APIResponseException(RequestException):
    """API Exception thrown a when response status code is 500 or greater"""

    def __str__(self):
        if self.response is not None:
            return str(self.response.json())
        return "Whoops! An error occurred..."


class APINotConfigured(IOError):
    """This API isn't configured correctly"""


################
# WALLET EXCEPTIONS
################


class WalletAPIException(APIResponseException):
    """Wallet API Exception thrown when a response status code is 500 or greater"""


class WalletAlreadyExistsException(WalletAPIException):
    pass


class WalletDoesNotExistException(WalletAPIException):
    pass


class WalletLockedException(WalletAPIException):
    pass


class WalletUnlockedException(WalletAPIException):
    pass


class WalletMissingPubKeyException(WalletAPIException):
    pass


class WalletInvalidPasswordException(WalletAPIException):
    pass


class WalletNotAvailableException(WalletAPIException):
    pass


class KeyExistsException(WalletAPIException):
    pass


class UnsupportedKeyTypeException(WalletAPIException):
    pass


class InvalidLockTimeoutException(WalletAPIException):
    pass


class SecureEnclaveExceptions(WalletAPIException):
    pass


################
# CHAIN EXCEPTIONS
################


class ChainAPIException(APIResponseException):
    """Chain API Exception thrown when a response status code is 500 or greater"""


# Authorization Exceptions


class AuthorizationException(ChainAPIException):
    pass


class DuplicateSignatureException(ChainAPIException):
    pass


class UnsatisfiedAuthException(ChainAPIException):
    pass


class MissingAuthException(ChainAPIException):
    pass


class IrrelevantAuthException(ChainAPIException):
    pass


class InsufficientDelayException(ChainAPIException):
    pass


class InvalidPermissionException(ChainAPIException):
    pass


class InvalidParentPermission(ChainAPIException):
    pass


# Resource Exceptions

class ResourceExhaustedException(ChainAPIException):
    pass


class RamUsageExceededException(ChainAPIException):
    pass


class TXNetUsageExceededException(ChainAPIException):
    pass


class BlockNetUsageExceededException(ChainAPIException):
    pass


class TXCPUUsageExceededException(ChainAPIException):
    pass


class BlockCPUUsageExceededException(ChainAPIException):
    pass


class DeadlineException(ChainAPIException):
    pass


class GreylistNetUsageExceeded(ChainAPIException):
    pass


# Transaction Exceptions


class TransactionException(ChainAPIException):
    pass


class DecompressionException(TransactionException):
    pass


class NoActionExceptions(TransactionException):
    pass


class NoAuthorizations(TransactionException):
    pass


class CFAAuthorizationException(TransactionException):
    pass


class ExpiredTXException(TransactionException):
    pass


class InvalidRefBlockException(TransactionException):
    pass


class DuplicateTXException(TransactionException):
    pass


class DuplicateDeferredTXException(TransactionException):
    pass


class CFAInsideGeneratedTXException(TransactionException):
    pass


class TXNotFoundException(TransactionException):
    pass


class TooManyTXException(TransactionException):
    pass


class TXTooBigException(TransactionException):
    pass


class UnknownCompression(TransactionException):
    pass


# Type Exceptions

class TypeException(ChainAPIException):
    pass


class NameTypeException(TypeException):
    pass


class PublicKeyTypeException(TypeException):
    pass


class PrivateKeyTypeException(TypeException):
    pass


class AuthorityTypeException(TypeException):
    pass


class ActionTypeException(TypeException):
    pass


class TransactionTypeException(TypeException):
    pass


class ABITypeException(TypeException):
    pass


class BlockIDTypeException(TypeException):
    pass


class TransactionIDTypeException(TypeException):
    pass


class PackedTransactionTypeException(TypeException):
    pass


class AssetTypeException(TypeException):
    pass


class ChainIDTypeException(TypeException):
    pass


class FixedKeyTypeException(TypeException):
    pass


class SymbolTypeException(TypeException):
    pass


################
# MODEL EXCEPTIONS
################


class ModelException(IOError):
    """Model Exception thrown when a model's validations fail"""


class PermissionDoesNotExistException(ModelException):
    """Permission DNE Exception thrown when a specified permission does not exist on a specified account"""


class AccountDoesNotExistException(ModelException):
    """Account DNE Exception thrown when a specified account_name does not exist"""


class AccountAlreadyExistsException(ModelException):
    """Account DNE Exception thrown when a specified account_name does not exist"""


class AccountABIDoesNotExistException(ModelException):
    """ABI DNE Exception thrown when an account does not have an ABI"""


class ActionDoesNotExistException(ModelException):
    """Action DNE Exception thrown when account ABI does not contain action_name"""
