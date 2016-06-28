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
            alpha=0.1, gamma=.5, strategy='e-greedy', epsilon=.25)

    def idle(self):
        """Update the QLearning table, retrieve an action and check for
        dead-ends.
        """
        action = self.learning_model.update(self.percept_).action

        if (all(s.imminent_collision for s in
                self.sensors['proximity'].values()) or
            self.cycle_ >= constants.MAX_LEARNING_CYCLES):
            # There's nothing left to be done, only flag this is a dead-end
            # so it can be restarted.
            self.state_ = STATES.stuck

        else:
            # Reduce step size if we are going against a close obstacle.
            sensors = self.sensors['proximity']

            sensor = (sensors['front'] if action == Actions.FORWARD else
                      sensors['back'] if action == Actions.BACKWARD else
                      None)

            stride = (min(self.STRIDE, .9 * sensor.distance) if sensor else
                      self.STRIDE)

            move_to = ((stride, 0, 0) if action == Actions.FORWARD else
                       (-stride, 0, 0) if action == Actions.BACKWARD else
                       self.INSTRUCTIONS_MAP[action])

            logger.info('walking: %s', move_to)
            self.motion.post.moveTo(*move_to)
            self.state_ = STATES.moving

        return self

    def moving(self):
        """Prevents the robot of thinking too much."""
        if not self.motion.moveIsActive():
            # motion.post.moveTo call is non-blocking. We wait until they
            # are finished and only then re-evaluate the environment.
            self.state_ = STATES.idle
