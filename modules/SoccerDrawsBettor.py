"""
SoccerDrawsBettor.py
"""

from BettingAnalyzer import BettingAnalyzer
from MatchMaker import MatchMaker
from NitrogenSession import NitrogenSession
from ResultEvaluator import ResultEvaluator
from SystemParameters import *

class SoccerDrawsBettor(object):
    """
    Main class of soccer draws betting system, orchestrates all others
    """

    def __init__(self):

        self.BettingAnalyzer = BettingAnalyzer()
        self.MatchMaker = MatchMaker()
        self.ResultEvaluator = ResultEvaluator()

        self.session = NitrogenSession()

        self.start()

    def start(self):
        """
        start
        """

        acct_balance = self.session.get_account_balance()
        self.BettingAnalyzer.set_balance(acct_balance)

        # continue_bets() will verify we have enough of a balance to start betting
        if self.BettingAnalyzer.continue_betting() is True:
            # TODO schedule find_next_bet in 1 second
            print('TODO schedule find_next_bet 1 second from now')

    def find_next_bet(self):
        """
        find_next_bet
        """

        next_bet = self.MatchMaker.find_next_bet()
        if next_bet is None:
            # schedule another find_next_bet for 90 minutes out
            pass
        else:
            # place the bet then set ResultEvaluator to watch it
            pass
