"""Tag Component.

Component that retrieves the current absolute position of an object in
the V-REP simulation.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from .base import Component
from ..utils import vrep

logger = logging.getLogger('mazerunner')


class Tag(Component):
    def __init__(self, link, component):
        super(Tag, self).__init__(link=link, component=component)

        errors, position = vrep.simxGetObjectPosition(
            self.adapter.link, self.adapter.handler, -1,
            vrep.simx_opmode_streaming)

        self.position = np.array(3 * [np.inf] if errors else position)

    def read(self):
        errors, position = vrep.simxGetObjectPosition(
            self.adapter.link, self.adapter.handler, -1,
            vrep.simx_opmode_buffer)

        self.position = np.array(3 * [100] if errors else position)
        return self
