import sys
sys.path.append('./nitrogen-sports-api')
from nitrogen import NitrogenApi

import logging
import os
import time

# global constants
MINUTES_TO_SECONDS = 60

logging.basicConfig(level=logging.INFO)

class SoccerDrawsSystem():
    """
    Betting system based on soccer match draws
    """

    # betting system parameters
    LOG_FILENAME = 'soccer_draws.log'
    DEFAULT_RETRY_TIME = 30 * MINUTES_TO_SECONDS
    FIND_BET_RETRY_TIME = 90 * MINUTES_TO_SECONDS
    BUFFER_TIME_BEFORE_GAMES = 5 * MINUTES_TO_SECONDS
    BETTING_UNIT = 0.001
    MIN_ODDS = 2.85
    MAX_ODDS = 3.45
    MAX_BET_TIER = 13
    BANKROLL_GOAL = None  # infinity

    def __init__(self, nitrogen_user, nitrogen_pass):

        # set Nitrogen credentials
        self.nitrogen_username = nitrogen_user
        self.nitrogen_password = nitrogen_pass

        self.initialize_logging()

        # declare these ahead of later usage
        self.api = None
        self.game_cache = None
        self.current_bet_tier = 1
        self.starting_balance = -1.0
        self.last_known_balance = -1.0
        self.bet_in_progress = False
        self.next_bet = None

    def initialize_logging(self):
        """
        Initialize logging
        """

        try:
            os.remove(self.LOG_FILENAME)
        except OSError:
            pass

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.LOG_FILENAME)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, msg):
        """
        Log given message with timestamp

        Args:
            msg (str): Message to log
        """

        self.logger.info(msg)

    def start(self):
        """
        Start betting system
        """

        self.log('Starting Nitrogen soccer draws betting system.')

        self.api = NitrogenApi()
        self.login()

        transaction_dump = self.api.get_transactions()
        self.starting_balance = float(transaction_dump['transactionData']['balance'])
        self.log('Starting account balance is ' + str(self.starting_balance) + ' BTC.')
        time.sleep(1)

        if float(transaction_dump['transactionData']['inplay']) >= self.BETTING_UNIT:
            self.log('Found there is already a bet in progress.')
            self.bet_in_progress = True
        else:
            self.log('Using default setting of no bet in progress.')

        self.log('Bet tier is at ' + str(self.current_bet_tier) + '.')

        self.api.logout()
        time.sleep(1)

        self.last_known_balance = self.starting_balance

        self.main_loop()

    def main_loop(self):
        """
        Main loop
        """

        while True:

            if self.bet_in_progress is False:

                if self.last_known_balance < self.get_bet_amount():
                    self.log('** Insufficient funds to proceed. **')
                    raise RuntimeError('Insufficient funds to proceed.')

                while True:
                    self.login()
                    self.games_cache = self.api.find_upcoming_games()
                    time.sleep(1)

                    self.find_next_bet()

                    if self.next_bet is None:
                        self.logout()
                        self.log('Sleeping for ' + str(self.FIND_BET_RETRY_TIME) + ' seconds...')
                        time.sleep(self.FIND_BET_RETRY_TIME)
                    else:
                        break

                # add bet for the indicated event and period
                self.log('Adding bet...')
                add_bet_response = self.api.add_bet(self.next_bet['event_id'], self.next_bet['period_id'], 'moneyline_draw')
                self.next_bet = None
                if 'data' in add_bet_response:
                    bet_id = add_bet_response['data'][0]['bet'][0]['bet_id']
                    self.log('Success, bet ID is ' + str(bet_id) + '.')
                    time.sleep(1)

                    # adjust risk to appropriate amount
                    current_bet = self.get_bet_amount()
                    self.log('Adjusting risk to ' + str(current_bet) + ' BTC...')
                    self.api.adjust_risk(bet_id, str(current_bet))
                    time.sleep(1)

                    self.log('Placing betslip...')
                    self.api.place_betslip()
                    time.sleep(1)

                    self.log('Confirming betslip...')
                    self.api.confirm_betslip()
                    time.sleep(1)

                    self.bet_in_progress = True
                    self.log('Bet in progress.')

                    # update last known balance since we've spent money
                    transaction_dump = self.api.get_transactions()
                    self.last_known_balance = float(transaction_dump['transactionData']['balance'])
                    self.log('Available account balance is now ' + str(self.last_known_balance) + ' BTC.')
                    time.sleep(1)
                else:
                    self.log('** Something went wrong adding bet. **')
                    raise RuntimeError('Something went wrong adding bet.')

            else:
                self.login()
                transaction_dump = self.api.get_transactions()
                current_balance = float(transaction_dump['transactionData']['balance'])
                current_money_inplay = float(transaction_dump['transactionData']['inplay'])
                
                self.log('Last known balance: ' + str(self.last_known_balance) + ' BTC')
                self.log('Current balance: ' + str(current_balance) + ' BTC')
                self.log('Current inplay: ' + str(current_money_inplay) + ' BTC')

                if current_money_inplay < self.BETTING_UNIT:
                    self.bet_in_progress = False
                    if current_balance > self.last_known_balance:
                        self.current_bet_tier = 1
                        self.log('Detected WIN, reset bet tier to 1.')
                    # TODO handle 'push' scenario
                    else:
                        self.current_bet_tier += 1
                        self.log('Detected LOSS, progress bet tier to ' + str(self.current_bet_tier) + '.')
                    self.last_known_balance = current_balance

            self.logout()

            if self.should_continue_betting() is False:
                self.log('Conditions met to cease betting, ending...')
                break
            else:
                # TODO in most cases we'll know when the bet was placed, appropriate the wait to that
                # TODO shouldn't be sleeping if we just progressed the bet tier
                self.log('Sleeping for ' + str(self.DEFAULT_RETRY_TIME) + ' seconds.')
                time.sleep(self.DEFAULT_RETRY_TIME)

    def get_bet_amount(self):
        """
        Get appropriate bet amount for current tier

        Returns:
            (float) Appropriate bet amount in Bitcoin
        """

        bet_amount = 1 * self.BETTING_UNIT
        working_bet_tier = self.current_bet_tier
        while working_bet_tier >= 4:
            bet_amount *= 1.5
            working_bet_tier -= 1
        while working_bet_tier >= 2:
            bet_amount *= 2.0
            working_bet_tier -= 1
        return bet_amount

    def find_next_bet(self):
        """
        Find next bet to place
        """

        MIN_CUTOFF = int(time.time()) + self.BUFFER_TIME_BEFORE_GAMES

        for event in self.games_cache['data']:
            event_id = event['event_id']
            for period in event['period']:
                period_id = period['period_id']
                if 'moneyLine' in period and period['moneyLine'] is not None:
                    if 'cutoffDateTime' in period and int(period['cutoffDateTime']) >= MIN_CUTOFF:
                        for line in period['moneyLine']:
                            if 'drawPrice' in line and line['drawPrice'] is not None:
                                draw_price = float(line['drawPrice'])
                                if draw_price >= self.MIN_ODDS and draw_price <= self.MAX_ODDS:
                                    self.log('Found bet at odds ' + str(draw_price) + ', event ID ' + event_id + ', period ID ' + period_id + '.')
                                    self.next_bet = {'event_id': event_id,
                                                     'period_id': period_id,
                                                     'bet_type': 'moneyline_draw',
                                                     'bet_id': '-1'}
                                    return
        # if we get here we didn't find a suitable bet
        self.log('Did not find suitable next bet.')

    def login(self):
        """
        Login
        """

        self.log('Logging in as ' + self.nitrogen_username + '...')
        self.api.login(self.nitrogen_username, self.nitrogen_password)
        time.sleep(1)

    def logout(self):
        """
        Logout
        """

        self.log('Logging out.')
        self.api.logout()

    def should_continue_betting(self):
        """
        Indicates whether betting should continue

        Returns:
            (bool)
        """

        return True

if __name__ == '__main__':

    BET_SYSTEM = SoccerDrawsSystem('flot989', 'Thr0wAway1')
    BET_SYSTEM.start()
