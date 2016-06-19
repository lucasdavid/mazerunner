"""Simple Navigator Example.

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

    ips_and_ports = zip(args.ip.split(' '), args.port.split(' '))

    robots = [Navigator('navigator-%i' % robot_id, (ip, port))
              for robot_id, (ip, port) in enumerate(ips_and_ports)]

    maze = mazerunner.Environment(agents=robots,
                                  update_period=2,
                                  life_cycles=args.iterations).live()
    print('Bye.')
