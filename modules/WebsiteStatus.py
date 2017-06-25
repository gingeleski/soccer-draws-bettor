"""
WebsiteStatus.py
"""

from Logger import Logger
from SystemParameters import UPTIME_MONITOR_KEY

import requests

UPTIME_ROBOT_STATUS_PAUSED = 0
UPTIME_ROBOT_STATUS_UNCHECKED = 1
UPTIME_ROBOT_STATUS_UP = 2
UPTIME_ROBOT_STATUS_SEEMS_DOWN = 8
UPTIME_ROBOT_STATUS_DOWN = 9

class WebsiteStatus(object):
    """
    Uses the UptimeRobot API to see if NitrogenSports site is up or down.

    If utilizing this, you must have a monitor set up beforehand and put the API key that's
    specifically for that monitor into SystemParameters.py
    """

    def __init__(self, active=True):
        self.active = active
        self.api_url = 'https://api.uptimerobot.com/v2/getMonitors'
        self.payload = 'api_key=' + UPTIME_MONITOR_KEY + '&format=json&logs=0'
        self.headers = {
            'content-type' : 'application/x-www-form-urlencoded',
            'cache-control' : 'no-cache'
        }

    def isWebsiteUp(self):
        """
        Checks to see if NitrogenSports is up

        Returns:
            (bool)
        """
        if self.active is False:
            return True

        res = requests.post(self.api_url, data=self.payload, headers=self.headers, verify=False)
        res_json = res.json()

        status_code = res_json['monitors'][0]['status']

        if status_code == UPTIME_ROBOT_STATUS_UP:
            return True

        Logger.logn('Reporting https://nitrogensports.eu as down')
        return False
