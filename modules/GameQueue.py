"""
GameQueue.py
"""

class GameQueue(object):
    """
    An auto-sorting data structure meant to hold game objects.

    Sorts based on cutoff time.

    When you 'get', it gives that first element and removes.

    """

    def __init__(self):
        self.queue = []

    def empty(self):
        """
        Is the queue empty?

        Returns:
            (bool)
        """

        if len(self.queue == 0):
            return True
        return False

    def get(self):
        """
        Return and remove the earliest cutoff time object

        Returns:
            (object)
        """

        if self.empty:
            return None
        to_return = self.queue[0]
        del self.queue[0]
        return to_return

    def put(self, game_data):
        """
        Add an object, inserting based on cutoff time

        """

        if self.empty() is True:
            # just plop in the queue if it's empty
            self.queue.append(game_data)
        else:
            # otherwise we have to figure out where it rightfully goes
            # TODO
            pass
