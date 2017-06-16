"""
NitrogenSession.py
"""

import os, sys
sys.path.append('.' + os.sep + 'modules' + os.sep + 'nitrogen-sports-api')
from nitrogen import NitrogenApi

from Logger import Logger
from SystemParameters import *

import time

class NitrogenSession(object):
    """
    Wraps the Nitrogen Sports API to abstract away nuances and logging statements
    """

    def __init__(self):

        self.api = NitrogenApi()

        self.logged_in = False
        self.last_login_time = -1

    def login(self):
        """
        Log in to Nitrogen Sports
        """

        self.api.login(NITROGEN_USER, NITROGEN_PASS)
        self.logged_in = True
        self.last_login_time = int(time.time())
        time.sleep(1)

    def logout(self):
        """
        Log out of Nitrogen Sports
        """

        self.api.logout()
        self.logged_in = False
        time.sleep(1)

    def freshen_session(self):
        """
        Ensure the session is fresh, either by logging in or taking other measures to avoid timeout
        """

        if self.logged_in is False:
            self.login()
        elif int(time.time()) - self.last_login_time >= HARD_SESSION_TIMEOUT:
            self.logout()
            self.login()

    def get_account_balance(self):
        """
        Get account balance in Bitcoin
        """

        self.freshen_session()

        transaction_dump = self.api.get_transactions()
        acct_balance = float(transaction_dump['transactionData']['balance'])
        Logger.log('Observing account balance at ' + str(acct_balance) + ' BTC.')

        return acct_balance

    def get_my_wagers(self):
        """
        Get 'My Wagers'
        """

        self.freshen_session()

        return self.api.get_my_wagers()

    def find_upcoming_games(self):
        """
        Get data dump of upcoming soccer games
        """

        self.freshen_session()

        return self.api.find_upcoming_games()

    def find_league_games(self, league_key):
        """
        Get dump of soccuer games for the given league

        Args:
            league_key (str)
        """

        self.freshen_session()

        return self.api.find_games(league=league_key)

    def add_and_confirm_bet(self, event_id, period_id, bet_type, amount_to_bet):
        """
        Goes through the whole process of adding and confirming a bet, which
        includes 4 different HTTP requests
        """

        self.freshen_session()

        add_bet_response = self.add_bet(event_id, period_id, bet_type)

        if 'data' in add_bet_response:
            bet_id = add_bet_response['data'][0]['bet'][0]['bet_id']
            Logger.log('Success, bet ID is ' + str(bet_id) + '.')
            time.sleep(1)

            # adjust risk to appropriate amount
            Logger.log('Adjusting risk to ' + str(amount_to_bet) + ' BTC...')
            self.adjust_risk(bet_id, amount_to_bet)
            time.sleep(1)

            Logger.log('Placing betslip...')
            self.place_betslip()
            time.sleep(1)

            Logger.log('Confirming betslip...')
            self.confirm_betslip()
            time.sleep(1)

            Logger.log('Bet in progress.')
        else:
            Logger.log('** Something went wrong adding bet. **')
            raise RuntimeError('Something went wrong adding bet.')

    def add_bet(self, event_id, period_id, bet_type):
        """
        add_bet
        """

        return self.api.add_bet(event_id, period_id, bet_type)

    def adjust_risk(self, bet_id, amount_to_bet):
        """
        adjust_risk
        """

        return self.api.adjust_risk(bet_id, str(amount_to_bet))

    def place_betslip(self):
        """
        place_betslip
        """

        return self.api.place_betslip()

    def confirm_betslip(self):
        """
        confirm_betslip
        """

        return self.api.confirm_betslip()
