"""
SystemParameters.py
"""

from datetime import datetime

_START_TIME_STR = datetime.now().strftime('m-%d-%Y_%H-%M-%S')
_MINUTES_TO_SECONDS = 60

LOGFILE_NAME = 'actions_' + _START_TIME_STR + '.log'
BET_DB_NAME = 'bets_' + _START_TIME_STR + '.db'

# Nitrogen Sports credentials
NITROGEN_USER = '<YOUR USERNAME>'
NITROGEN_PASS = '<YOUR PASSWORD>'

####################################################################################################

####################################################################################################
# RISK MATH

# Range into which the odds of a match draw must fall
MIN_ODDS = 2.85
MAX_ODDS = 3.45

# Base betting unit in Bitcoin
BETTING_UNIT = 0.001

# How many losses before we give up
MAX_BET_TIER = 13

# How much of a bet to place on each tier
BET_VALUE_GUIDE = {}
BET_VALUE_GUIDE[1] = 1 * BETTING_UNIT
BET_VALUE_GUIDE[2] = BET_VALUE_GUIDE[1] * 2
BET_VALUE_GUIDE[3] = BET_VALUE_GUIDE[2] * 2
BET_VALUE_GUIDE[4] = BET_VALUE_GUIDE[3] * 1.5
BET_VALUE_GUIDE[5] = BET_VALUE_GUIDE[4] * 1.5
BET_VALUE_GUIDE[6] = BET_VALUE_GUIDE[5] * 1.5
BET_VALUE_GUIDE[7] = BET_VALUE_GUIDE[6] * 1.5
BET_VALUE_GUIDE[8] = BET_VALUE_GUIDE[7] * 1.5
BET_VALUE_GUIDE[9] = BET_VALUE_GUIDE[8] * 1.5
BET_VALUE_GUIDE[10] = BET_VALUE_GUIDE[9] * 1.5
BET_VALUE_GUIDE[11] = BET_VALUE_GUIDE[10] * 1.5
BET_VALUE_GUIDE[12] = BET_VALUE_GUIDE[11] * 1.5
BET_VALUE_GUIDE[13] = BET_VALUE_GUIDE[12] * 1.5

####################################################################################################

####################################################################################################
# WAIT TIMES

# How long, in seconds, to try looking for a match again if we don't find one
FIND_BET_RETRY_TIME = 90 * _MINUTES_TO_SECONDS

HARD_SESSION_TIMEOUT = 5 * _MINUTES_TO_SECONDS
