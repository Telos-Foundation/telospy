import pytest
from eospython.api import API

# TODO: Test assumes that a chain exists on localhost, and that a TIP-5 contract exists


class TestContract(object):

    def __init__(self):
        API('http://localhost:8888')
        self.contract_account = 'goodblockio1'