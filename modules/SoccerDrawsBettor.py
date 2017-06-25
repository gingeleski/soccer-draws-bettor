"""
SoccerDrawsBettor.py
"""

from BettingAnalyzer import BettingAnalyzer
from Logger import Logger
from MatchMaker import MatchMaker
from NitrogenSession import NitrogenSession
from ResultEvaluator import ResultEvaluator
from SystemParameters import *
from WebsiteStatus import WebsiteStatus

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
        self.WebsiteStatus = WebsiteStatus(DO_UPTIME_MONITORING)

        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.session = NitrogenSession()

        self.start()

    def start(self):
        """
        Start
        """

        self.check_website_status()

        acct_balance = self.session.get_account_balance()
        self.BettingAnalyzer.set_balance(acct_balance)

        # Use continue_bets() to verify we have enough $$$
        if self.BettingAnalyzer.continue_betting() is False:
            raise Exception('Insufficient funds to start betting.')

        self.scheduler.enter(1 * SECONDS, 1, self.find_next_bet)
        self.scheduler.run()

    def find_next_bet(self):
        """
        Find next bet
        """

        self.check_website_status()

        next_bet = self.MatchMaker.find_next_bet(self.session)
        if next_bet is None:
            # Schedule another find_next_bet after the specified retry time
            Logger.logn('next_bet is none, scheduling a retry...')
            self.scheduler.enter(FIND_BET_RETRY_TIME, 1, self.find_next_bet)
        else:
            Logger.logn('Going to place the following bet...')
            Logger.logn(next_bet)
            game_cutoff_time = next_bet['cutoff_time']
            amount_to_bet = self.BettingAnalyzer.get_current_bet_amount()
            self.MatchMaker.place_bet(self.session, next_bet, amount_to_bet)

            # Load the bet into ResultEvaluator
            self.ResultEvaluator.acquire_target(self.session)

            # Check on the game status around when it'll probably be over
            first_game_check_time = game_cutoff_time + ESTIMATED_GAME_TIME - int(time.time())
            self.scheduler.enter(first_game_check_time, 1, self.check_on_bet)

    def check_on_bet(self):
        """
        Check on a bet in progress, see if there's yet a result
        """

        self.check_website_status()

        game_bet_outcome = self.ResultEvaluator.get_status(self.session)

        if game_bet_outcome == 'PENDING':
            self.scheduler.enter(BET_RECHECK_TIME, 1, self.check_on_bet)
            return
        elif game_bet_outcome == 'WIN':
            self.BettingAnalyzer.reset_betting_level()
        elif game_bet_outcome == 'LOSS':
            self.BettingAnalyzer.progress_betting_level()
        elif game_bet_outcome == 'DRAW':
            pass
        else:
            raise RuntimeError('Received unsupported game bet outcome')

        self.scheduler.enter(1 * SECONDS, 1, self.find_next_bet)

    def check_website_status(self):
        """
        Check that Nitrogen Sports site is up, halting bot if needed
        """

        while self.WebsiteStatus.isWebsiteUp() is False:
            Logger.logn('NitrogenSports is down, rechecking in ' + str(WEBSITE_DOWN_RECHECK_TIME) + ' seconds')
            time.sleep(WEBSITE_DOWN_RECHECK_TIME)
