"""Proximity Sensor.

An abstraction for the proximity sensor in V-REP.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from .base import Sensor
from .. import utils

logger = logging.getLogger('mazerunner')


class ProximitySensor(Sensor):
    """Proximity Sensor.

    An abstraction for the proximity sensor in V-REP.
    
    """

    COLLISION_THRESHOLD = .2

    def __init__(self, link, component):
        super(ProximitySensor, self).__init__(link, component=component)

        data = utils.vrep.simxReadProximitySensor(
            self.adapter.link, self.adapter.handler,
            utils.vrep.simx_opmode_streaming)
        self.last_read = data[1:]

    def read(self):
        """Retrieve the Proximity Sensor Reading.

        :return: tuple (detected, point, handler, normal_v)
        or None if an error occurred.
        """
        data = utils.vrep.simxReadProximitySensor(
            self.adapter.link, self.adapter.handler,
            utils.vrep.simx_opmode_buffer)

        if data[0] != 0:
            logger.warning('error detecting proximity sensor (%s)', data[0])

        self.last_read = data[1:]
        return self

    @property
    def imminent_collision(self):
        """Checks if this sensor is in an imminent collision,
        based on a pre-defined threshold.

        :return bool: True, if it is about to collide. False, otherwise.
        """
        return self.distance <= self.COLLISION_THRESHOLD

    @property
    def distance(self):
        """Retrieve the distance between the base of the sensor's 
        position frame and the detected point in space.

        If last reading didn't detect any collision, returns the overflowing
        value 100.

        """
        detected, point = self.last_read[:2]
        return np.linalg.norm(point) if detected else 1
