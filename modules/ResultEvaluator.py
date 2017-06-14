"""
ResultsEvaluator.py
"""

class ResultEvaluator(object):
    """
    Determines whether match outcome was win, loss, draw, or still pending
    """

    def __init__(self):
        self.target_bet_id = None

    def acquire_target(self, nitro_session):
        """
        acquire_target

        Args:
            nitro_session (NitrogenSession) - Session to retrieve wager data with
        """

        wagers_dump = nitro_session.get_my_wagers()

        for data_obj in wagers_dump['data']:
            for bet_obj in data_obj['bet']:
                if bet_obj['result'] == 'Pending':
                    self.target_bet_id = str(bet_obj['bet_id'])
                    return

        raise RuntimeError('Could not acquire target bet')

    def get_status(self, nitro_session):
        """
        get_status

        Args:
            nitro_session (NitrogenSession) - Session to retrieve wager data with
        """

        wagers_dump = nitro_session.get_my_wagers()

        for data_obj in wagers_dump['data']:
            for bet_obj in data_obj['bet']:
                if str(bet_obj['bet_id']) == self.target_bet_id:
                    if bet_obj['result'].lower() == 'pending':
                        return 'PENDING'
                    raise RuntimeError('Encountered unknown result status ' + bet_obj['result'])

        for data_obj in wagers_dump['data_graded']:
            for bet_obj in data_obj['bet']:
                if str(bet_obj['bet_id']) == self.target_bet_id:
                    if bet_obj['result'].lower() == 'lose':
                        return 'LOSS'
                    elif bet_obj['result'].lower() == 'win':
                        return 'WIN'
                    elif bet_obj['result'].lower() == 'push':
                        return 'PUSH'
                    elif bet_obj['result'].lower() == 'draw':
                        return 'PUSH'
                    else:
                        raise RuntimeError('Encountered unknown result status ' + bet_obj['result'])

        raise RuntimeError('Lost track of bet (ID ' + self.target_bet_id + ', could not get status')
