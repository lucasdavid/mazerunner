"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

from . import base

logger = logging.getLogger('mazerunner')


class Walker(base.RoboticAgent):
    """Walker Agent.

    An robotic agent that walks randomly, avoiding walls.
    """

    speed = 0.3 #old speed=1.0

    def idle(self):
        self.motion.moveToward(self.speed, 0, 0)
        self.state_ = self.States.moving

    def moving(self):
        if any(s.imminent_collision for s in self.sensors['proximity']):
            self.motion.stopMove()
            self.posture.goToPosture('Stand', 1)
            self.state_ = self.States.thinking

    def thinking(self): pass
    def disabled(self): pass
    def dead(self): pass
