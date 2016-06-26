"""MazeRunner Constants.

Constants shared by all sub-modules.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from enum import Enum

STATES = Enum('disabled', 'idle', 'moving', 'thinking', 'stuck', 'dead')
ACTIONS = Enum('forward', 'backward', 'clockwise', 'cclockwise')
