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
