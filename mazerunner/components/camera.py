"""Camera Sensor.

A component that retrieves images from a vision sensor in the V-REP simulation.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from .base import Sensor
from ..utils import vrep


class Camera(Sensor):
    """Camera Sensor."""
    def __init__(self, link, component):
        super(Camera, self).__init__(link, component)

        errors, resolution, image = vrep.simxGetVisionSensorImage(
            self.adapter.link, self.adapter.handler, 0,
            vrep.simx_opmode_streaming)

        self.image = image

    def read(self):
        errors, resolution, image = vrep.simxGetVisionSensorImage(
            self.adapter.link, self.adapter.handler, 0,
            vrep.simx_opmode_buffer)

        self.image = image
        return self
