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
        time.sleep(1)
        self.logged_in = True

    def logout(self):
        """
        Log out of Nitrogen Sports
        """

        self.api.logout()
        time.sleep(1)
        self.logged_in = False

    def freshen_session(self):
        """
        Make sure the session is fresh, either by logging in or otherwise taking measures to avoid timeout
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
