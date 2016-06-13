"""Simple Walker Example.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

import mazerunner
from mazerunner.agents import Walker
from mazerunner.base.arguments import client_parser
from mazerunner.utils import live

logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print(__doc__)
    args = client_parser.parse_args()

    runners = [Walker(args.ip, args.port)]
    maze = mazerunner.Environment(agents=runners, update_rate=1)

    try:
        live(maze, iterations=args.iterations)
    except KeyboardInterrupt:
        pass
    finally:
        print('Bye.')
