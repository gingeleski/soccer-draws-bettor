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
PING_URL_START = 'socket.io/?EIO=3&transport=polling'

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
        self.polling_sid = None
        self.ping_interval = -1
        self.ping_count = 0
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
        """

        login_url = BASE_URL + 'php/login/login.php'
        payload = {'username': username, 'password': password, 'otp': '', 'captcha_code': ''}
        req = self.session.post(login_url, data=payload, verify=False)
        if req.status_code == requests.codes.ok:
            self.authenticated = True
        else:
            raise RuntimeError('Response to #login not OK')

    def logout(self):
        """
        Logout
        """

        logout_url = BASE_URL + 'php/login/logout.php'
        req = self.session.post(logout_url, verify=False)
        if req.status_code != requests.codes.ok:
            print(req.text)
            raise RuntimeError('Response to #logout not OK')
        else:
            self.authenticated = False

    def ping(self):
        """
        Send the server heartbeat / keep-alive / ping
        """

        unix_time = int(time.time())
        ping_url = BASE_URL + PING_URL_START + '&t=' + str(unix_time)
        ping_url = ping_url + '-' + str(self.ping_count)
        req = None
        if self.ping_count == 0:
            req = self.session.get(ping_url, verify=False)
            poll_info_json = json.loads(req.text[req.text.find('{'):])
            self.polling_sid = poll_info_json['sid']
            self.ping_interval = poll_info_json['pingInterval'] / 1000
        else:
            ping_url = ping_url + '&sid=' + self.polling_sid
            if self.ping_count < 3:
                req = self.session.get(ping_url, verify=False)
            else:
                req = self.session.post(ping_url, verify=False)
        if req is None or req.status_code != requests.codes.ok:
            print(req.text)
            raise RuntimeError('Response to #ping not OK')
        self.ping_count += 1

    def keep_alive(self, duration=None):
        """
        Keep the session alive by pinging at a normal interval

        Args:
            duration: how long to keep alive, in seconds
        """

        now = int(time.time())
        if duration is not None:
            end_time = now + duration
        else:
            end_time = None
        next_time = now
        looping = True
        while looping is True:
            if duration is not None and now > end_time:
                looping = False
            elif now >= next_time:
                self.ping()
                next_time = now + self.ping_interval
            time.sleep(1)
            now = int(time.time())

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
