"""Agent Base.

Basic definitions, such as the Agent and RoboticAgent base classes.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
from enum import Enum
from naoqi import ALProxy
import numpy as np

from mazerunner.components.base import Adapter
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

    States = Enum('disabled', 'idle', 'moving', 'thinking', 'stuck', 'dead')

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 random_state=None):
        super(RoboticAgent, self).__init__()

        if len(interface) != 2:
            raise ValueError('Invalid interface: %s' % str(interface))

        self.identity = identity
        self.interface = interface
        self.random_state = random_state or np.random.RandomState()

        self.motion = ALProxy("ALMotion", *interface)
        self.posture = ALProxy("ALRobotPosture", *interface)

        self.adapter = Adapter(link, 'NAO') if link else None
        self.sensors = dict()

        self.joint_manager_ = None
        self.state_ = self.States.disabled
        self.percept_ = None

    def start(self, link=None):
        if link is not None:
            self.adapter = Adapter(link, 'NAO')

        self.motion.wakeUp()
        self.posture.goToPosture('Stand', .5)

        self.joint_manager_ = utils.JointManager(link=self.adapter.link,
                                                 motion=self.motion,
                                                 identity=self.identity)
        self.joint_manager_.start()

        self.sensors['vision'] = {
            'front': components.Camera(self.adapter.link,
                                       component='NAO_vision1'),
            'floor': components.Camera(self.adapter.link,
                                       component='NAO_vision2'),
        }

        self.sensors['proximity'] = {
            'front': components.ProximitySensor(self.adapter.link,
                                                component='Proximity_sensor1'),
            'left': components.ProximitySensor(self.adapter.link,
                                               component='Proximity_sensor2'),
            'right': components.ProximitySensor(self.adapter.link,
                                                component='Proximity_sensor3'),
            'back': components.ProximitySensor(self.adapter.link,
                                               component='Proximity_sensor4'),
        }

        self.sensors['distance'] = {
            'start': components.Tag(self.adapter.link, component='tag1'),
            'goal': components.Tag(self.adapter.link, component='tag2'),
            'self': components.Tag(self.adapter.link, component='tag3')
        }

        self.state_ = self.States.idle

    def perceive(self):
        for tag, camera in self.sensors['vision'].items():
            camera.read()

        sensor_distances = []
        for tag, sensor in self.sensors['proximity'].items():
            sensor.read()
            sensor_distances.append(sensor.distance)

        # Get starting point, goal and robot positions.
        start, goal, me = (np.array(p.position)
                           for p in self.sensors['distance'].values())

        # Assemble perceived state structure.
        self.percept_ = [np.linalg.norm(goal - me)] + sensor_distances

        logger.info(str(self.percept_))

        return self

    def act(self):
        """Find a method with the same name of its current state and execute
        it.
        """
        return getattr(self, str(self.state_))()

    def stuck(self):
        """Reset agent to the starting point."""
        logger.info('Agent is stuck. Transporting it to the starting point.')

        self.motion.stopMove()
        self.posture.goToPosture('Stand', .5)

        self.state_ = self.States.idle

    def dead(self):
        """Doesn't do anything."""

    def dispose(self):
        self.motion.stopMove()
        self.posture.goToPosture('Stand', .5)

        # Stop sync routine.
        self.joint_manager_.active_ = False
        self.joint_manager_.join()

        self.state_ = self.States.dead

        return self
