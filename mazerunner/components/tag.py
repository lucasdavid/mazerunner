"""Tag Component.

Component that retrieves the current absolute position of an object in
the V-REP simulation.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

from .base import Component
from ..utils import vrep

logger = logging.getLogger('mazerunner')


class Tag(Component):
    def __init__(self, link, component):
        super(Tag, self).__init__(link=link, component=component)

        errors, position = vrep.simxGetObjectPosition(
            self.adapter.link, self.adapter.handler, -1,
            vrep.simx_opmode_streaming)

    @property
    def position(self):
        errors, position = vrep.simxGetObjectPosition(
            self.adapter.link, self.adapter.handler, -1,
            vrep.simx_opmode_buffer)

        return None if errors else position
