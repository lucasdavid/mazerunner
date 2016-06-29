"""Navigate.

Navigate through the house looking for the kitchen.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

import mazerunner
from mazerunner.agents import Navigator

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

INTERFACE = ('127.0.0.1', 5000)
UPDATE_PERIOD = 0.5 #2
ITERATIONS = None

if __name__ == "__main__":
    print(__doc__)

    mazerunner.Environment(
        agents=[Navigator(0, interface=INTERFACE)],
        update_period=UPDATE_PERIOD,
        life_cycles=ITERATIONS).live()

    print('Bye.')
