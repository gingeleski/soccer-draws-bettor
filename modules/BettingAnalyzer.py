"""
BettingAnalyzer.py
"""

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

    def set_balance(self, new_balance):
        """
        Set account balance
        """

        self.balance = new_balance

    def continue_betting(self):
        """
        Evaluates whether betting can and should continue

        Returns:
            (bool)
        """

        if BET_VALUE_GUIDE[self.current_betting_level] > self.balance:
            return False
        return True
        