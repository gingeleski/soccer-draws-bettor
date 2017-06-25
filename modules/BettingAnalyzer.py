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

        Logger.logn('Initialized BettingAnalyzer at ' + str(self.start_time))

    def set_balance(self, new_balance):
        """
        Set account balance
        """

        self.current_balance = new_balance
        if self.start_balance is None:
            self.start_balance = self.current_balance
            Logger.logn('Starting balance recorded as ' + str(self.start_balance) + ' BTC')

    def reset_betting_level(self):
        """
        Reset current betting level to 1
        """

        self.current_betting_level = 1
        Logger.logn('Bet level reset to ' + str(self.current_betting_level))

    def progress_betting_level(self):
        """
        Progress current betting level by 1
        """

        Logger.logn('Progressing bet level...')
        self.current_betting_level += 1
        if self.current_betting_level > MAX_BET_TIER:
            Logger.logn('Max betting level exceeded')
            raise RuntimeError('Max betting level exceeded')
        Logger.logn('Bet level is at ' + str(self.current_betting_level))

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

        out = 'Start time: ' + str(self.start_time)
        out += '\n' + 'Start balance: ' + str(self.start_balance) + ' BTC'
        out += '\n' + 'End time: ' + str(self.end_time)
        out += '\n' + 'End balance: ' + str(self.end_balance) + ' BTC'

        # TODO implement the following...
        out += '\n' + 'Total profit: XX BTC'
        out += '\n' + 'Mean profit per day: XX BTC'
        out += '\n' + 'Mean profit per hour: XX BTC'
        out += '\n' + 'Total risked: XX BTC'
        out += '\n' + 'Average number of bets before a win: XX'
        out += '\n' + 'Average profit per win: XX BTC'

        with open(OUTPUT_PATH + ANALYTICS_FILE_NAME, 'w') as file:
            file.write(out)

    def __del__(self):
        self.end_time = int(time.time())
        self.end_balance = self.current_balance
        self.write_analysis_file()
        