"""MazeRunner Navigator Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

from . import Walker
from .. import constants, learning
from ..constants import STATES, Actions

logger = logging.getLogger('mazerunner')


class Navigator(Walker):
    """Navigator Agent."""

    STRIDE = 1
    SPEED = .7

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 learning_model=None, random_state=None):
        super(Navigator, self).__init__(identity, interface, link, random_state)

        self.learning_model = learning_model or learning.QLearning(
            alpha=0.2, gamma=.75, strategy='e-greedy', epsilon=.85)

    def idle(self):
        """Update the QLearning table, retrieve an action and check for
        dead-ends.
        """
        action = self.learning_model.update(self.percept_).action

        if (all(s.imminent_collision for s in
                self.sensors['proximity']) or
                self.cycle_ >= constants.MAX_LEARNING_CYCLES):
            # There's nothing left to be done, only flag this is a dead-end
            # so it can be restarted.
            self.state_ = STATES.stuck

        else:
            sensors = self.sensors['proximity']

            sensor = (sensors[0] if action == Actions.FORWARD else
                      sensors[1] if action == Actions.BACKWARD else
                      None)

            stride = self.STRIDE
            if sensor and sensor.imminent_collision:
                # Reduce step size if it's going against a close obstacle.
                stride = min(stride, .9 * sensor.distance)

            move_to = ((stride, 0, 0) if action == Actions.FORWARD else
                       (-stride, 0, 0) if action == Actions.BACKWARD else
                       self.INSTRUCTIONS_MAP[action])

            logger.info('walking: %s', move_to)
            self.motion.post.moveTo(*move_to)
            self.state_ = STATES.moving

        return self

    def moving(self):
        """Makes sure the robot completes its actions before requesting
        a new one to its QLearning model."""
        if not self.motion.moveIsActive():
            # motion.post.moveTo call is non-blocking. We wait until they
            # are finished and only then re-evaluate the environment.
            self.state_ = STATES.idle
