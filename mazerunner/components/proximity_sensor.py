"""Proximity Sensor.

An abstraction for the proximity sensor in V-REP.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

from .base import Sensor
from ..utils import vrep

logger = logging.getLogger('mazerunner')


class ProximitySensor(Sensor):
    """Proximity Sensor.

    An abstraction for the proximity sensor in V-REP.
    """

    tag = 'Proximity_sensor'

    def __init__(self, link, component_id=''):
        super(ProximitySensor, self).__init__(link, component_id)

        data = vrep.simxReadProximitySensor(self.link, self.adapter,
                                            vrep.simx_opmode_streaming)

        self.last_read = data[1:]

    def read(self):
        errors, detected, point, handler, normal_v = \
            vrep.simxReadProximitySensor(self.link, self.adapter,
                                         vrep.simx_opmode_buffer)
        self.last_read = (detected, point, normal_v)
        logger.info('proximity sensor: %s', str(self.last_read))
        return self.last_read

    @property
    def imminent_collision(self):
        return self.last_read and self.last_read[0]
