"""MazeRunner Navigator Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""

import logging

from . import Walker
from .. import constants, learning
from ..constants import STATES, ACTION_SELECTION

logger = logging.getLogger('mazerunner')


class Navigator(Walker):
    """Navigator Agent."""

    STRIDE = .2

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 learning_model=None, random_state=None):
        super(Navigator, self).__init__(identity, interface, link, random_state)

        self.learning_model = learning_model or learning.QLearning(
            gamma=.5,
            action_selection=ACTION_SELECTION.e_greedy,
            action_selection_epsilon=0.25)

    def idle(self):
        """Update the QLearning table, retrieve an action and check for
        dead-ends.
        """
        self.learning_model.set_state(self.percept_)
        action = self.learning_model.action

        logger.info('action to be performed: %s', action)

        if (all(s.imminent_collision for s in
                self.sensors['proximity'].values()) or
            self.cycle_ >= constants.MAX_LEARNING_CYCLES):
            # There's nothing left to be done, only flag this is a dead-end
            # so it can be restarted.
            self.state_ = STATES.stuck

        else:
            # min(s.distance for tag, s in self.sensors['proximity'].items() if tag in ('front', 'back'))
            logger.info('About to walk %s', self.INSTRUCTIONS_MAP[action])
            self.motion.post.moveTo(*self.INSTRUCTIONS_MAP[action])
            self.state_ = STATES.moving

        return self

    def moving(self):
        """Prevents the robot of thinking too much."""
        if not self.motion.moveIsActive():
            # motion.post.moveTo call is non-blocking. We wait until they
            # are finished and only then re-evaluate the environment.
            self.state_ = STATES.idle
