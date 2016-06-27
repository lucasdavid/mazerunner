"""MazeRunner Constants.

Constants shared by all sub-modules.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from enum import Enum


class ACTIONS:
    forward = 0
    backward = 1
    clockwise = 2
    cclockwise = 3

STATES = Enum('disabled', 'idle', 'moving', 'thinking', 'stuck', 'dead')

