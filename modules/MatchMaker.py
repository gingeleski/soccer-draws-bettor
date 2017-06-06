"""
MatchFinder.py
"""

from SystemParameters import *

import time

class MatchMaker(object):
    """
    Give us a match to bet on
    """

    def __init__(self):
        pass

    def find_next_bet(self, nitro_session):
        """
        find_next_bet

        Args:
            nitro_session (NitrogenSession) - Session to retrieve game data with
        """

        games_cache = nitro_session.find_upcoming_games()

        MIN_CUTOFF = int(time.time()) + BUFFER_TIME_BEFORE_GAMES

        for event in games_cache['data']:
            event_id = event['event_id']
            for period in event['period']:
                period_id = period['period_id']
                if 'moneyLine' in period and period['moneyLine'] is not None:
                    if 'cutoffDateTime' in period and int(period['cutoffDateTime']) >= MIN_CUTOFF:
                        for line in period['moneyLine']:
                            if 'drawPrice' in line and line['drawPrice'] is not None:
                                draw_price = float(line['drawPrice'])
                                if draw_price >= MIN_ODDS and draw_price <= MAX_ODDS:
                                    return {'event_id': event_id,
                                            'period_id': period_id,
                                            'bet_type': 'moneyline_draw',
                                            'bet_id': '-1'}

        # if we get here we didn't find a suitable bet
        return None
