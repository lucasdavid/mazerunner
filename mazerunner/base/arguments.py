"""MazeRunner Arguments.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import argparse

client_parser = argparse.ArgumentParser()
client_parser.add_argument('--ip', type=str, default='127.0.0.1',
                           help='Robot ip address')
client_parser.add_argument('--port', type=int, default=5000,
                           help='Robot port number')
client_parser.add_argument('--iterations', type=int, default=100,
                           help='Number of iterations')
