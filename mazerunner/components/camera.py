from .base import Sensor
from ..utils import vrep


class Camera(Sensor):
    tag = 'NAO_vision'

    def __init__(self, link, component_id=''):
        super(Camera, self).__init__(link, component_id)

        errors, resolution, image = vrep.simxGetVisionSensorImage(
            self.link, self.adapter, 0, vrep.simx_opmode_streaming)

        self.last_read = image

    def read(self):
        errors, resolution, image = vrep.simxGetVisionSensorImage(
            self.link, self.adapter, 0, vrep.simx_opmode_buffer)

        self.last_read = image
        return image
