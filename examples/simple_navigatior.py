"""Simple Navigator Example.

In this example, the agent navigates through the scene, looking for its goal.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

import mazerunner
from mazerunner.agents import Navigator
from mazerunner.base.arguments import client_parser

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print(__doc__)
    args = client_parser.parse_args()

    runners = [Navigator(args.ip, args.port)]
    maze = mazerunner.Environment(agents=runners, update_period=2,
                                  life_cycles=args.iterations).live()
    print('Bye.')
