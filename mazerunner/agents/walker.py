"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import numpy as np
import logging

from . import base

logger = logging.getLogger('mazerunner')


class Walker(base.RoboticAgent):
    """Walker Agent.

    An robotic agent that walks randomly, avoiding walls.
    """

    STRIDE = 1.0

    def idle(self):
        """Initiates the robot movement."""
        self.state_ = self.States.moving

    def moving(self):
        """Move the robot's body , preventing collisions on its way out.
        If there're obstacles on the way, rotates appropriately.

        """
        if self.motion.moveIsActive():
            # Doesn't do anything until the movement is complete. Collision
            # checking isn't necessary, as movements are only started when the
            # sensors indicate a free path.
            pass

        elif not self.sensors['proximity']['front'].imminent_collision:
            # Walker will always keep moving forward,
            # if no obstacles are found.
            self.motion.post.moveTo(self.STRIDE, 0, 0)

        else:
            self.motion.stopMove()
            self.posture.goToPosture('Stand', 1)

            if not self.sensors['proximity']['left'].imminent_collision:
                # Rotate to the left.
                self.motion.post.moveTo(0, 0, np.pi / 2)

            elif not self.sensors['proximity']['right'].imminent_collision:
                # Rotate to the right.
                self.motion.post.moveTo(0, 0, -np.pi / 2)

            elif not self.sensors['proximity']['back'].imminent_collision:
                # Go back.
                self.motion.post.moveTo(0, 0, -np.pi)

            else:
                # There's nothing to do. Flag this is a dead-end.
                self.state_ = self.States.stuck
