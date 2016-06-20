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

    MAX_SPEED = 1
    speed = 1

    def __init__(self, identity='', interface=('127.0.0.1', 5000)):
        super(Walker, self).__init__(identity, interface)

        self._imminent_collision = False

    def idle(self):
        self.motion.moveToward(self.speed, 0, 0)

        self.state_ = self.States.moving

    def moving(self):
        if any(s.imminent_collision for s in self.sensors['proximity']):
            self.motion.stopMove()
            self.posture.goToPosture('Stand', 1)
            self.state_ = self.States.thinking

    def thinking(self): pass

    def dispose(self):
        super(Walker, self).dispose()
        self.motion.stopMove()
        self.posture.goToPosture('Stand', 1)

        return self
