"""
MatchFinder.py
"""

from GameQueue import GameQueue
from SystemParameters import *

import queue
import time

class MatchMaker(object):
    """
    Give us a match to bet on
    """

    def __init__(self):
        self.game_cache = GameQueue()

    def find_next_bet(self, nitro_session):
        """
        find_next_bet

        Args:
            nitro_session (NitrogenSession) - Session to retrieve game data with
        """

        min_cutoff_time = int(time.time()) + BUFFER_TIME_BEFORE_GAMES

        # cache just the games starting soon
        games_json = nitro_session.find_upcoming_games()
        self.interpret_games_json(games_json, min_cutoff_time)

        min_cutoff_time = int(time.time()) + BUFFER_TIME_BEFORE_GAMES
        this_game = self.game_cache.get()

        while this_game is not None:
            if this_game['cutoff_time'] >= min_cutoff_time:
                return this_game
            this_game = self.game_cache.get()

        # if we struck out there, cache games from nearly all soccer leagues
        for league_key in SOCCER_GAME_DATA_KEYS:
            min_cutoff_time = int(time.time()) + BUFFER_TIME_BEFORE_GAMES

            games_json = nitro_session.find_league_games(league_key)
            self.interpret_games_json(games_json, min_cutoff_time)

        min_cutoff_time = int(time.time()) + BUFFER_TIME_BEFORE_GAMES
        this_game = self.game_cache.get()

        while this_game is not None:
            if this_game['cutoff_time'] >= min_cutoff_time:
                return this_game
            this_game = self.game_cache.get()

    def place_bet(self, nitro_session):
        """
        place_bet
        """

        print('Adding bet...')

        # TODO there's a world of todo's in here, do them

        event_id = 'TODO'
        period_id = 'TODO'
        add_bet_response = nitro_session.add_bet(event_id, period_id, 'moneyline_draw')

        if 'data' in add_bet_response:
            bet_id = add_bet_response['data'][0]['bet'][0]['bet_id']
            #self.log('Success, bet ID is ' + str(bet_id) + '.')
            time.sleep(1)

            # adjust risk to appropriate amount
            #current_bet = self.get_bet_amount()
            #print('Adjusting risk to ' + str(current_bet) + ' BTC...')
            #self.api.adjust_risk(bet_id, str(current_bet))
            time.sleep(1)

            print('Placing betslip...')
            #self.api.place_betslip()
            time.sleep(1)

            print('Confirming betslip...')
            #self.api.confirm_betslip()
            time.sleep(1)

            #self.bet_in_progress = True
            print('Bet in progress.')

            # update last known balance since we've spent money
            #transaction_dump = self.api.get_transactions()
            #self.last_known_balance = float(transaction_dump['transactionData']['balance'])
            #print('Available account balance is now ' + str(self.last_known_balance) + ' BTC.')
            time.sleep(1)
        else:
            print('** Something went wrong adding bet. **')
            raise RuntimeError('Something went wrong adding bet.')

    def interpret_games_json(self, games_json, min_cutoff_time):
        """
        interpret_games_json
        """

        for event in games_json['data']:
            event_id = event['event_id']
            for period in event['period']:
                period_id = period['period_id']
                if 'moneyLine' in period and period['moneyLine'] is not None:
                    if 'cutoffDateTime' in period:
                        cutoff_time = int(period['cutoffDateTime'])
                        if cutoff_time >= min_cutoff_time:
                            for line in period['moneyLine']:
                                if 'drawPrice' in line and line['drawPrice'] is not None:
                                    draw_price = float(line['drawPrice'])
                                    if draw_price >= MIN_ODDS and draw_price <= MAX_ODDS:
                                        game_data = {'cutoff_time' : cutoff_time,
                                                     'event_id' : event_id,
                                                     'period_id' : period_id,
                                                     'bet_type' : 'moneyline_draw',
                                                     'bet_id' : '-1'}
                                        self.game_cache.put(game_data)
