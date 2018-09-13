#    _                _                      _ __    _  _
#   | |_     ___     | |     ___     ___    | '_ \  | || |
#   |  _|   / -_)    | |    / _ \   (_-<    | .__/   \_, |
#   _\__|   \___|   _|_|_   \___/   /__/_   |_|__   _|__/
# _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_| """"|
# "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'


import logging

logger = logging.getLogger()
# TODO: setup a method for switching the code from development to production
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

