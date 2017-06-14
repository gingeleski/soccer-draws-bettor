"""
NitrogenSession.py
"""

import os, sys
sys.path.append('.' + os.sep + 'modules' + os.sep + 'nitrogen-sports-api')
from nitrogen import NitrogenApi

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
        return float(transaction_dump['transactionData']['balance'])

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
