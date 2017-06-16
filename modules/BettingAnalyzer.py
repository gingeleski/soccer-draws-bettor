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
        self.balance = 0.0
        self.current_betting_level = 1
        self.start_time = int(time.time())
        Logger.log('Initializing BettingAnalyzer at ' + str(self.start_time))

    def set_balance(self, new_balance):
        """
        Set account balance
        """

        self.balance = new_balance

    def reset_betting_level(self):
        """
        Reset current betting level to 1
        """

        self.current_betting_level = 1

    def progress_betting_level(self):
        """
        Progress current betting level by 1
        """

        Logger.log('Progressing bet level...')
        self.current_betting_level += 1
        if self.current_betting_level > MAX_BET_TIER:
            Logger.log('Max betting level exceeded.')
            raise RuntimeError('Max betting level exceeded.')
        Logger.log('Bet level is at ' + str(self.current_betting_level) + '.')

    def get_current_bet_amount(self):
        """
        Get the appropriate amount to bet at our current level
        """

        return BET_VALUE_GUIDE[self.current_betting_level]

    def continue_betting(self):
        """
        Evaluates whether betting can and should continue

        Returns:
            (bool)
        """

        if BET_VALUE_GUIDE[self.current_betting_level] > self.balance:
            return False
        return True
        