"""
SystemParameters.py
"""

from datetime import datetime

_START_TIME_STR = datetime.now().strftime('m-%d-%Y_%H-%M-%S')
_MINUTES_TO_SECONDS = 60

LOGFILE_NAME = 'actions_' + _START_TIME_STR + '.log'
BET_DB_NAME = 'bets_' + _START_TIME_STR + '.db'

# Base betting unit in Bitcoin
BETTING_UNIT = 0.001

# How long, in seconds, to try looking for a match again if we don't find one
FIND_BET_RETRY_TIME = 90 * _MINUTES_TO_SECONDS

# How many losses before we give up
MAX_BET_TIER = 13

# Range for the odds of a match draw to meet our system
MIN_ODDS = 2.85
MAX_ODDS = 3.45
