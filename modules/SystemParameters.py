"""
SystemParameters.py
"""

from datetime import datetime

_START_TIME_STR = datetime.now().strftime('m-%d-%Y_%H-%M-%S')

# The following are constants to represent times in seconds
SECONDS = 1
MINUTES = 60

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
FIND_BET_RETRY_TIME = 90 * MINUTES

# What's the nearest cutoff time for a new bet we're evaluating? Give system enough time to bet
BUFFER_TIME_BEFORE_GAMES = 2 * MINUTES

HARD_SESSION_TIMEOUT = 5 * MINUTES

####################################################################################################

####################################################################################################
# SOCCER GAME DATA KEYS

SOCCER_GAME_DATA_KEYS = []
SOCCER_GAME_DATA_KEYS += 'UEFA+-+U21+European+Championship'
SOCCER_GAME_DATA_KEYS += 'USA+-+Major+League+Soccer'
SOCCER_GAME_DATA_KEYS += 'USA+-+Major+League+Soccer+Corners'
SOCCER_GAME_DATA_KEYS += 'International+-+Friendlies'
SOCCER_GAME_DATA_KEYS += 'International+-+Friendlies+Corners'
SOCCER_GAME_DATA_KEYS += 'Spain+-+Segunda+Liga'
SOCCER_GAME_DATA_KEYS += 'Italy+-+Serie+B'
SOCCER_GAME_DATA_KEYS += 'Algeria+-+Professional+Ligue+1'
SOCCER_GAME_DATA_KEYS += 'Algeria+-+Youth+U21+League'
SOCCER_GAME_DATA_KEYS += 'Argentina+-+Cup'
SOCCER_GAME_DATA_KEYS += 'Argentina+-+Primera+B+Nacional'
SOCCER_GAME_DATA_KEYS += 'Argentina+-+Primera+B+Nacional+Corners'
SOCCER_GAME_DATA_KEYS += 'Argentina+-+Primera+Division'
SOCCER_GAME_DATA_KEYS += 'Argentina+-+Primera+Division+Corners'
SOCCER_GAME_DATA_KEYS += 'Bolivia+-+LFPB'
SOCCER_GAME_DATA_KEYS += 'Brazil+-+U20'
SOCCER_GAME_DATA_KEYS += 'China+-+Super+League'
SOCCER_GAME_DATA_KEYS += 'Club+Friendlies'
SOCCER_GAME_DATA_KEYS += 'FIFA+-+World+Cup+U20'
SOCCER_GAME_DATA_KEYS += 'FIFA+-+Confed+Cup'
SOCCER_GAME_DATA_KEYS += 'Germany+-+Oberliga'
SOCCER_GAME_DATA_KEYS += 'Germany+-+Regionalliga+Cup'
SOCCER_GAME_DATA_KEYS += 'International+-+Friendlies+U21+Corners'
SOCCER_GAME_DATA_KEYS += 'International+-+Friendlies+U21'
SOCCER_GAME_DATA_KEYS += 'Ireland+-+Premier'
SOCCER_GAME_DATA_KEYS += 'Jamaica+-+Premier+League'
SOCCER_GAME_DATA_KEYS += 'Lithuania+-++A+Lyga'
SOCCER_GAME_DATA_KEYS += 'Romania+-+Liga+1'
SOCCER_GAME_DATA_KEYS += 'Venezuela+-+Primera+Division'
SOCCER_GAME_DATA_KEYS += 'USA+-+North+American+Soccer+League'
SOCCER_GAME_DATA_KEYS += 'Austria+-+Regionalliga+Mitte'
SOCCER_GAME_DATA_KEYS += 'Austria+-+Regionalliga'
SOCCER_GAME_DATA_KEYS += 'Australia+NPL+-+Western+Australia'
SOCCER_GAME_DATA_KEYS += 'Australia+NPL+-+Victoria'
SOCCER_GAME_DATA_KEYS += 'Australia+NPL+-+South+Australia'
SOCCER_GAME_DATA_KEYS += 'Australia+NPL+-+New+South+Wales'
SOCCER_GAME_DATA_KEYS += 'Australia+-+Women+League'
SOCCER_GAME_DATA_KEYS += 'Australia+-+Victoria+Premier+League+Women'
SOCCER_GAME_DATA_KEYS += 'Australia+-+National+Youth+League'
SOCCER_GAME_DATA_KEYS += 'Australia+-+FFA+Cup+Qualifiers'
SOCCER_GAME_DATA_KEYS += 'Australia+-+FFA+Cup'
SOCCER_GAME_DATA_KEYS += 'Australia+-+Brisbane+Premier+League'
SOCCER_GAME_DATA_KEYS += 'Australia+-+Brisbane+Capital+League+1'
