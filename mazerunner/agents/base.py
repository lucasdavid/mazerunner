"""Agent Base.

Basic definitions, such as the Agent and RoboticAgent base classes.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
from enum import Enum
from naoqi import ALProxy

from .. import components, utils

logger = logging.getLogger('mazerunner')


class Agent(object):
    """Agent Base."""

    def update(self):
        self.perceive()
        self.act()

    def perceive(self):
        raise NotImplementedError

    def act(self):
        raise NotImplementedError


class RoboticAgent(Agent):
    """Robot Agent Base.

    :param identity: [str, int], default=''.
        Integer or string that identifies the robot that will be controlled.
        E.g.: 0, '', 'jogger' or 'kyle'.

    :param interface: tuple (str, int).
        Tuple indicating the IP and port of the robot that will be controlled.
        E.g.: ('127.0.0.1', 5000), ('localhost', 6223).
    """

    States = Enum('disabled', 'idle', 'moving', 'thinking', 'dead')

    def __init__(self, identity='', interface=('127.0.0.1', 5000)):
        super(RoboticAgent, self).__init__()

        if len(interface) != 2:
            raise ValueError('Invalid interface: %s' % str(interface))

        self.identity = identity
        self.interface = interface

        self.motion = ALProxy("ALMotion", *interface)
        self.posture = ALProxy("ALRobotPosture", *interface)

        self.sensors = dict()

        self.link_ = None
        self.joint_manager_ = None
        self.state_ = self.States.disabled

    def start(self, link):
        self.link_ = link

        self.motion.wakeUp()
        self.posture.goToPosture('Stand', .5)

        self.joint_manager_ = utils.JointManager(link=self.link_,
                                                 motion=self.motion,
                                                 identity=self.identity)
        self.joint_manager_.start()

        self.sensors['vision'] = (
            components.Camera(link, component_id=1),
            components.Camera(link, component_id=2),
        )

        self.sensors['proximity'] = (
            components.ProximitySensor(link, component_id=1),
        )

        self.state_ = self.States.idle

    def perceive(self):
        for camera in self.sensors['vision']: camera.read()
        for sensor in self.sensors['proximity']: sensor.read()

        return self

    def act(self):
        """Find a method with the same name of its current state and execute
        it.
        """
        return getattr(self, str(self.state_))()

    def dispose(self):
        self.motion.stopMove()
        self.posture.goToPosture('Stand', .5)

        # Stop sync routine.
        self.joint_manager_.active_ = False
        self.joint_manager_.join()

        self.state_ = self.States.dead

        return self
