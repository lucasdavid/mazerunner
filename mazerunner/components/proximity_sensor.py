"""Proximity Sensor.

An abstraction for the proximity sensor in V-REP.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from .base import Sensor
from ..utils import vrep

logger = logging.getLogger('mazerunner')


class ProximitySensor(Sensor):
    """Proximity Sensor.

    An abstraction for the proximity sensor in V-REP.
    """

    def __init__(self, link, component):
        super(ProximitySensor, self).__init__(link, component=component)

        data = vrep.simxReadProximitySensor(
            self.adapter.link, self.adapter.handler,
            vrep.simx_opmode_streaming)
        self.last_read = data[1:]

    def read(self):
        """Retrieve the Proximity Sensor Reading.

        :return: tuple (detected, point, handler, normal_v)
        or None if an error occurred.
        """
        data = vrep.simxReadProximitySensor(
            self.adapter.link, self.adapter.handler,
            vrep.simx_opmode_buffer)
        self.last_read = None if data[0] else data[1:]
        return self.last_read

    @property
    def imminent_collision(self):
        """Checks If This Sensor is In Imminent Collision.

        :return bool: True, if it is about to collide. False, otherwise.
        """
        return self.last_read and self.last_read[0]

    @property
    def distance(self):
        detected, point = self.last_read[:2]
        return np.linalg.norm(point) if detected else 100
