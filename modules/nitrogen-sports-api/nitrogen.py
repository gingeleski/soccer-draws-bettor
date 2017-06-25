import cfscrape

import json
import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util.retry import Retry

# Suppress HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = 'https://nitrogensports.eu/'

class NitrogenApi():
    """
    Interface to programmatically interact with Nitrogen Sports
    """

    def __init__(self, auto_start_session=True):
        """
        Constructor
        """

        self.authenticated = False
        self.session = None

        if auto_start_session is True:
            self.new_session()

    def new_session(self):
        """
        Launch a new session
        """

        self.session = cfscrape.CloudflareScraper()

        retries = Retry(total=5, backoff_factor=1)
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        self.pass_cloudflare()

    def pass_cloudflare(self):
        """
        Complete the Cloudflare check for this session
        """

        self.session.get(BASE_URL, verify=False)

    def login(self, username=None, password=None):
        """
        Login

        Returns:
            (tuple) - [0] status (str), [1] balance (float), [2] inplay (float)
        """

        login_url = BASE_URL + 'php/login/login.php'
        payload = {'username': username, 'password': password, 'otp': '', 'captcha_code': ''}

        status = 'PENDING'
        req = self.session.post(login_url, data=payload, verify=False)

        if req.status_code != requests.codes.ok:
            status = 'NOT OK'
            return status, None, None

        self.authenticated = True

        status = 'SUCCESS'
        balance = req.json()['balance']
        inplay = req.json()['inplay']

        return status, balance, inplay

    def logout(self):
        """
        Logout

        Returns:
            status (str)
        """

        logout_url = BASE_URL + 'php/login/logout.php'

        status = 'PENDING'
        req = self.session.post(logout_url, verify=False)

        if req.status_code != requests.codes.ok:
            status = 'NOT OK'
            return status

        status = 'SUCCESS'
        self.authenticated = False

        return status

    def get_transactions(self):
        """
        Get user's transactions
        """

        get_url = BASE_URL + 'php/query/getupdates.php?transactions_timestamp='
        req = self.session.post(get_url, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #get_transactions not OK')

    def get_betslip(self):
        """
        Get current betslip
        """

        get_url = BASE_URL + 'php/query/betslip_get.php'
        req = self.session.post(get_url, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #get_betslip not OK')

    def add_bet(self, event_id, period_id, bet_type, bet_id='-1'):
        """
        Adds a bet to the betslip

        Args:
            event_id (str): Event ID num string (i.e. '711667105')
            period_id (str): Period ID num string (i.e. '387060156')
            bet_type (str): Bet type string (i.e. 'moneyline_draw')
            bet_id (str): Bet ID num string if applicable (default '-1')
        """

        add_url = BASE_URL + 'php/query/betslip_addBet.php'
        payload = {'event_id': event_id, 'period_id': period_id, \
                    'bet_type': bet_type, 'bet_id': bet_id}
        req = self.session.post(add_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #add_bet not OK')

    def adjust_risk(self, bet_id=None, risk=None):
        """
        Adjusts risk of a bet on the betslip

        Args:
            bet_id (int): Which bet to adjust
            risk (float): Target Bitcoin risk amount
        """

        adjust_url = BASE_URL + 'php/query/betslip_bet_adjustRisk.php'
        payload = {'bet_id': bet_id, 'risk': risk}
        req = self.session.post(adjust_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #adjust_risk not OK')

    def place_betslip(self):
        """
        Place betslip
        """

        place_url = BASE_URL + 'php/query/betslip_get_place.php'
        req = self.session.post(place_url, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #place_betslip not OK')

    def confirm_betslip(self, betslip_type='straight'):
        """
        Confirm betslip
        """

        confirm_url = BASE_URL + 'php/query/betslip_confirm.php'
        payload = {'betslip_type': betslip_type, 'teaser_id': 0, 'coupon_id': ''}
        req = self.session.post(confirm_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #confirm_betslip not OK')

    def find_upcoming_games(self, sport='Soccer'):
        """
        Request upcoming games for the given sport
        """

        games_url = BASE_URL + 'php/query/findgames_upcomming.php'
        payload = {'sport': sport}
        req = self.session.post(games_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #find_upcoming_games not OK')

    def find_games(self, sport='Soccer', league='', period_description=''):
        """
        Request games for the given sport and league
        """

        games_url = BASE_URL + 'php/query/findgames.php'
        payload = {'sport' : sport,
                   'league' : league,
                   'period_description': period_description}
        req = self.session.post(games_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #find_games not OK')

    def get_my_wagers(self):
        """
        Get 'My Wagers'
        """

        wagers_url = BASE_URL + 'php/query/mywagers.php'
        req = self.session.post(wagers_url, verify=False)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            print(req.text)
            raise RuntimeError('Response to #get_my_wagers not OK')
