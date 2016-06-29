"""MazeRunner Respawner Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""

import logging

from . import Walker
from ..constants import STATES

logger = logging.getLogger('mazerunner')


class Respawner(Walker):
    """Respawner Agent.

    This is a toy agent that exemplifies how a RoboticAgent behaves when
    stuck by easily reaching this state.

    """

    def idle(self):
        sensors = self.sensors['proximity']
        if any(s.imminent_collision for s in sensors):
            self.state_ = STATES.stuck

        else:
            self.motion.post.moveTo(self.STRIDE, 0, 0)
            self.state_ = STATES.moving

        return self

    def moving(self):
        if not self.motion.moveIsActive():
            self.state_ = STATES.idle
