"""
SoccerDrawsBettor.py
"""

from BettingAnalyzer import BettingAnalyzer
from MatchMaker import MatchMaker
from NitrogenSession import NitrogenSession
from ResultEvaluator import ResultEvaluator
from SystemParameters import *

import sched
import time

class SoccerDrawsBettor(object):
    """
    Main class of soccer draws betting system, orchestrates all others
    """

    def __init__(self):

        self.BettingAnalyzer = BettingAnalyzer()
        self.MatchMaker = MatchMaker()
        self.ResultEvaluator = ResultEvaluator()

        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.session = NitrogenSession()

        self.start()

    def start(self):
        """
        start
        """

        acct_balance = self.session.get_account_balance()
        self.BettingAnalyzer.set_balance(acct_balance)

        # use continue_bets() to verify we have enough $$$
        if self.BettingAnalyzer.continue_betting() is False:
            raise Exception('Insufficient funds to start betting.')

        self.scheduler.enter(1 * SECONDS, 1, self.find_next_bet)
        self.scheduler.run()

    def find_next_bet(self):
        """
        find_next_bet
        """

        next_bet = self.MatchMaker.find_next_bet(self.session)
        if next_bet is None:
            # schedule another find_next_bet after the specified retry time
            print('next_bet is none, scheduling a retry...')
            self.scheduler.enter(FIND_BET_RETRY_TIME, 1, self.find_next_bet)
        else:
            # TODO place the bet
            print('Would place the following bet...')
            print(next_bet)
            # TODO must set this `game_cutoff_time` var
            game_cutoff_time = -1
            #self.MatchMaker.place_bet(...

            # Load the bet into ResultEvaluator
            ###self.ResultEvaluator.acquire_target(self.session)

            # Check on the game status around when it'll probably be over
            first_game_check_time = game_cutoff_time + ESTIMATED_GAME_TIME - int(time.time())
            self.scheduler.enter(first_game_check_time, 1, self.check_on_bet)

    def check_on_bet(self):
        """
        check_on_bet
        """

        game_bet_outcome = self.ResultEvaluator.get_status(self.session)

        if game_bet_outcome == 'PENDING':
            self.scheduler.enter(BET_RECHECK_TIME, 1, self.check_on_bet)
        elif game_bet_outcome == 'WIN':
            pass  # TODO
        elif game_bet_outcome == 'LOSS':
            pass  # TODO
        elif game_bet_outcome == 'DRAW':
            pass  # TODO
        else:
            raise RuntimeError('Received unsupported game bet outcome')
