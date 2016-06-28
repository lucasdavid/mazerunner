"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from . import base
from ..constants import Actions, STATES

logger = logging.getLogger('mazerunner')


class Walker(base.RoboticAgent):
    """Walker Agent.

    An robotic agent that walks randomly, avoiding walls.
    """

    STRIDE = 1.0
    SPEED = .7

    INSTRUCTIONS_MAP = {
        Actions.FORWARD: (STRIDE, 0, 0),
        Actions.BACKWARD: (-STRIDE, 0, 0),
        Actions.CLOCKWISE: (0, 0, -np.pi / 2),
        Actions.CCLOCKWISE: (0, 0, np.pi / 2),
    }

    def idle(self):
        """Initiates the robot movement."""
        self.state_ = STATES.moving

    def moving(self):
        """Move the robot's body forward until an obstacle is detected."""
        if self.sensors['proximity']['front'].imminent_collision:
            self.motion.stopMove()
            self.posture.goToPosture('Stand', self.SPEED)
            self.state_ = STATES.thinking

        elif not self.motion.moveIsActive():
            # Walker will always keep moving forward,
            # if no obstacles are found.
            forward = self.INSTRUCTIONS_MAP[Actions.FORWARD]
            self.motion.post.moveTo(*forward)

    def thinking(self):
        """Deliberate to avoid obstacles on the path."""
        if self.motion.moveIsActive():
            # Maneuver occurring. Let's finish it
            # before taking any other measure.
            pass

        elif not self.sensors['proximity']['front'].imminent_collision:
            # Goes back to moving state.
            self.state_ = STATES.moving

        elif all(s.imminent_collision for s in
                 self.sensors['proximity'].values()):
            # There's nothing left to be done, only flag this is a dead-end.
            self.state_ = STATES.stuck

        else:
            for sensor, maneuver in (('left', np.pi / 2),
                                     ('right', -np.pi / 2),
                                     ('back', np.pi)):
                # Find which direction doesn't have 
                # any obstacles and rotate to face it.
                if not self.sensors['proximity'][sensor].imminent_collision:
                    self.motion.post.moveTo(0, 0, maneuver)
                    break

        return self
