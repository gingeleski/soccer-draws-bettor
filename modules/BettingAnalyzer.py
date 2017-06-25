"""
BettingAnalyzer.py
"""

from Logger import Logger
from SystemParameters import *

import time

class BettingAnalyzer(object):
    """
    Keeps bet history, provides related statistics
    """

    def __init__(self):
        self.current_balance = 0.0
        self.current_betting_level = 1
        self.start_time = int(time.time())
        self.start_balance = None
        self.end_time = None
        self.end_balance = None

        Logger.log('Initialized BettingAnalyzer at ' + str(self.start_time))

    def set_balance(self, new_balance):
        """
        Set account balance
        """

        self.current_balance = new_balance
        if self.start_balance is None:
            self.start_balance = self.current_balance
            Logger.log('Starting balance recorded as ' + str(self.start_balance) + ' BTC')

    def reset_betting_level(self):
        """
        Reset current betting level to 1
        """

        self.current_betting_level = 1
        Logger.log('Bet level reset to ' + str(self.current_betting_level))

    def progress_betting_level(self):
        """
        Progress current betting level by 1
        """

        Logger.log('Progressing bet level...')
        self.current_betting_level += 1
        if self.current_betting_level > MAX_BET_TIER:
            Logger.log('Max betting level exceeded')
            raise RuntimeError('Max betting level exceeded')
        Logger.log('Bet level is at ' + str(self.current_betting_level))

    def get_current_bet_amount(self):
        """
        Get the appropriate amount in Bitcoin to bet at our current level

        Returns:
            (float)
        """

        return BET_VALUE_GUIDE[self.current_betting_level]

    def continue_betting(self):
        """
        Evaluates whether betting can and should continue

        Returns:
            (bool)
        """

        if BET_VALUE_GUIDE[self.current_betting_level] > self.current_balance:
            return False
        return True

    def write_analysis_file(self):
        """
        Writes an analytics file about this betting session
        """

        out = ''
        out += 'Start time: ' + str(self.start_time)
        out += 'Start balance: ' + str(self.start_balance) + ' BTC'
        out += 'End time: ' + str(self.end_time)
        out += 'End balance: ' + str(self.end_balance) + ' BTC'

        # TODO implement the following...
        out += 'Total profit: XX BTC'
        out += 'Mean profit per day: XX BTC'
        out += 'Mean profit per hour: XX BTC'
        out += 'Total risked: XX BTC'
        out += 'Average number of bets before a win: XX'
        out += 'Average profit per win: XX BTC'

        with open(OUTPUT_PATH + LOGFILE_NAME, 'w') as file:
            file.write(out)

    def __del__(self):
        self.end_time = int(time.time())
        self.end_balance = self.current_balance
        self.write_analysis_file()
        