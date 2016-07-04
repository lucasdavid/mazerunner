"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from . import base

logger = logging.getLogger('mazerunner')


class Walker(base.RoboticAgent):
    """Walker Agent.

    An robotic agent that walks randomly, avoiding walls.
    """

    STRIDE = 1
    SPEED = .7

    def idle(self):
        """Initiates the robot movement."""
        self.behavior_ = self.BEHAVIORS.moving

    def moving(self):
        """Move the robot's body forward until an obstacle is detected."""
        if self.sensors['proximity'][0].imminent_collision:
            self.motion.stopMove()
            self.posture.goToPosture('Stand', self.SPEED)
            self.behavior_ = self.BEHAVIORS.thinking

        elif not self.motion.moveIsActive():
            # Walker will always keep moving forward,
            # if no obstacles are found.
            move_to = (self.STRIDE, 0, 0)
            self.motion.post.moveTo(*move_to)
            logger.info('Walking: %s', move_to)

    def thinking(self):
        """Deliberate to avoid obstacles on the path."""
        if self.motion.moveIsActive():
            # Maneuver occurring. Let's finish it
            # before taking any other measure.
            pass

        elif not self.sensors['proximity'][0].imminent_collision:
            # Goes back to moving state.
            self.behavior_ = self.BEHAVIORS.moving

        elif all(s.imminent_collision for s in self.sensors['proximity']):
            # There's nothing left to be done, only flag this is a dead-end.
            self.behavior_ = self.BEHAVIORS.stuck

        else:
            peripheral_sensors = self.sensors['proximity'][1:]
            for maneuver, sensor in zip(range(1, 4), peripheral_sensors):
                if not sensor.imminent_collision:
                    # A sensor that indicates no obstacles were found.
                    # Move in that direction.
                    self.motion.post.moveTo(0, 0, np.pi / 2)
                    break

        return self
