import numpy as np

from .base import Sensor
from ..utils import vrep


class Compass(Sensor):
    def __init__(self, link, component):
        super(Sensor, self).__init__(link, component)

        errors, o = vrep.simxGetObjectOrientation(self.adapter.link,
                                                  self.adapter.handler, -1,
                                                  vrep.simx_opmode_streaming)
        self.orientation = o

    def read(self):
        errors, o = vrep.simxGetObjectOrientation(self.adapter.link,
                                                  self.adapter.handler,
                                                  -1, vrep.simx_opmode_buffer)
        self.orientation = o
        return self

    @property
    def is_lying_on_the_ground(self):
        """Checks if object referenced by compass is lying on the ground.

        "Lying on the ground" entails the compass is turned upside/downside
        or sideways. That is, rotate by `pi/2` degrees around the `x`
        axis minus a small "just-in-case" error of `.1`.
        """
        if self.orientation is None:
            return False

        return abs(self.orientation[0]) > .9 * np.pi / 2
