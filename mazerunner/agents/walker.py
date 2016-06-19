"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

from enum import Enum

from . import base
from ..utils import vrep

logger = logging.getLogger('mazerunner')


class Walker(base.RoboticAgent):
    """Walker Agent.

    An robotic agent that walks randomly, avoiding walls.
    """

    MAX_SPEED = 1
    speed = 1
    # perception = {}

    @property
    def in_imminent_collision(self):
        # return self.perception['sonar/left'] < .2 or
        # self.perception['sonar/right'] < .2
        return False

    def perceive(self):
        # self.perception['sonar/left'] = self.memory.getData(
        #     'Device/SubDeviceList/US/Left/Sensor/Value')
        # logger.info('left sonar: %s', str(self.perception['sonar/left']))
        #
        # self.perception['sonar/right'] = self.memory.getData(
        #     'Device/SubDeviceList/US/Right/Sensor/Value')
        # logger.info('right sonar: %s', str(self.perception['sonar/right']))
        # res1, visionSensorHandle = vrep.simxGetObjectHandle(
        #     self.link, 'NAO_vision1', vrep.simx_opmode_oneshot_wait)
        #
        # res2, resolution, image = vrep.simxGetVisionSensorImage(
        #     self.link, visionSensorHandle, 0, vrep.simx_opmode_streaming)

        return self

    def idle(self):
        self.motion.moveToward(self.speed, 0, 0)

        self.state_ = self.States.moving

    def moving(self):
        if self.in_imminent_collision:
            self.motion.stopMove()
            self.motion.rest()
            self.state_ = self.States.thinking

    def thinking(self):
        pass

    def dispose(self):
        super(Walker, self).dispose()
        self.motion.stopMove()
        self.motion.rest()

        return self
