"""MazeRunner Navigator Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import numpy as np

from . import Walker
from ..learning import QLearning

from ..constants import STATES


class Navigator(Walker):
    """Navigator Agent."""

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 learning_model=None, random_state=None):
        super(Navigator, self).__init__(identity, interface, link, random_state)

        self.learning_model = learning_model or QLearning()

    def idle(self):
        """Update the QLearning table, retrieve an action and check for
        dead-ends.
        """
        self.learning_model.setState(self.percept_)
        action = self.learning_model.getAction()

        print('action=', action)

        if all(s.imminent_collision for s in
               self.sensors['proximity'].values()):
            # There's nothing left to be done, only flag this is a dead-end
            # so it can be restarted.
            self.state_ = STATES.stuck

        else:
            instruction = self.INSTRUCTIONS_MAP[action]
            self.motion.moveTo(*action)
            self.state_ = STATES.moving

        return self

    def moving(self):
        """Prevents the robot of thinking too much."""
        if not self.motion.moveIsActive():
            # motion.post.moveTo call is non-blocking. We wait until they
            # are finished and only then re-evaluate the environment.
            self.state_ = STATES.idle
