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


class AGENT_STATES:
    close = 0
    faraway = 1
    collision = 2
    closetogoal = 10
    sameplace = 11
    movedaway = 12


class ACTION_SELECTION:
    greedy = 0,
    e_greedy = 1


STATES = Enum('disabled', 'idle', 'moving', 'thinking', 'stuck', 'dead')

