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
    Wraps the Nitrogen Sports API to abstract away fault tolerance, logging and nuances...
    """

    def __init__(self):

        self.api = NitrogenApi()

        self.logged_in = False
        self.last_login_time = None

        self.last_observed_balance = None
        self.last_observed_inplay = None

    def login(self):
        """
        Log in to Nitrogen Sports
        """

        attempts = 0

        while True:
            status, balance, inplay = self.api.login(NITROGEN_USER, NITROGEN_PASS)
            if status == 'SUCCCESS':
                self.logged_in = True
                self.last_login_time = int(time.time())
                self.last_observed_balance = balance
                self.last_observed_inplay = inplay
                time.sleep(1)
                return
            elif attempts < 3:
                attempts += 1
                time.sleep(120)  # Try again in 2 minutes
            else:
                Logger.log('** Could not log in without error **')
                raise RuntimeError('Could not log in without error')

    def logout(self):
        """
        Log out of Nitrogen Sports
        """

        attempts = 0

        while True:
            status = self.api.logout()
            if status == 'SUCCESS':
                self.logged_in = False
                time.sleep(1)
                return
            elif attempts < 3:
                attempts += 1
                time.sleep(120)  # Try again in 2 minutes
            else:
                Logger.log('** Could not log out without error **')
                raise RuntimeError('Could not log out without error')

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

        balance = self.last_observed_balance
        Logger.log('Recording account balance as ' + str(balance) + ' BTC')

        return balance

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

        attempts = 0

        while True:
            time.sleep(2)
            data = self.api.find_upcoming_games()
            if data['errno'] == 0:
                return data
            elif attempts < 3:
                attempts += 1
                time.sleep(120)  # Try again in 2 minutes
            else:
                Logger.log('** Could not get upcoming games without error **')
                raise RuntimeError('Could not get upcoming games without error')

    def find_league_games(self, league_key):
        """
        Get dump of soccuer games for the given league

        Args:
            league_key (str)

        Returns:
            (object)
        """

        self.freshen_session()

        attempts = 0

        while True:
            time.sleep(2)
            data = self.api.find_games(league=league_key)
            if data['errno'] == 0:
                return data
            elif attempts < 3:
                attempts += 1
                time.sleep(120)  # Try again in 2 minutes
            else:
                Logger.log('** Could not get league games without error **')
                raise RuntimeError('Could not get league games without error.')

    def add_and_confirm_bet(self, event_id, period_id, bet_type, amount_to_bet):
        """
        Goes through the whole process of adding and confirming a bet, which
        includes 4 different HTTP requests
        """

        self.freshen_session()

        add_bet_response = self.add_bet(event_id, period_id, bet_type)

        if 'data' in add_bet_response:
            bet_id = add_bet_response['data'][0]['bet'][0]['bet_id']
            Logger.log('Bet ID is ' + str(bet_id))
            time.sleep(1)
            self.adjust_risk(bet_id, amount_to_bet)
            time.sleep(1)
            self.place_betslip()
            time.sleep(1)
            self.confirm_betslip()
            time.sleep(1)
        else:
            Logger.log('** Something went wrong adding bet **')
            raise RuntimeError('Something went wrong adding bet')

        Logger.log('Bet in progress.')

    def add_bet(self, event_id, period_id, bet_type):
        """
        Add bet

        Returns:
            (object)
        """

        Logger.log('Adding bet... event ID ' + str(event_id) + ', period ID ' + str(period_id))
        return self.api.add_bet(event_id, period_id, bet_type)

    def adjust_risk(self, bet_id, amount_to_bet):
        """
        Adjust risk

        Returns:
            (object)
        """

        Logger.log('Adjusting bet ID ' + str(bet_id) + ' risk to ' + str(amount_to_bet) + ' BTC')
        return self.api.adjust_risk(bet_id, str(amount_to_bet))

    def place_betslip(self):
        """
        Place betslip

        Returns:
            (object)
        """

        Logger.log('Placing betslip...')
        return self.api.place_betslip()

    def confirm_betslip(self):
        """
        Confirm betslip
        
        Returns:
            (object)
        """

        Logger.log('Confirming betslip...')
        return self.api.confirm_betslip()
