"""Simple Walker Example.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

import mazerunner
from mazerunner.agents import Navigator

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

ROBOT_INTERFACES = [
    ('127.0.0.1', 5000),
]

ITERATIONS = None

if __name__ == "__main__":
    print(__doc__)

    maze = mazerunner.Environment(
        agents=[Navigator(i, interface)
                for i, interface in enumerate(ROBOT_INTERFACES)],
        update_period=2,
        life_cycles=ITERATIONS).live()

    print('Bye.')
