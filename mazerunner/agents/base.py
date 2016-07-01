"""Agent Base.

Basic definitions, such as the Agent and RoboticAgent base classes.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import numpy as np

from naoqi import ALProxy

from mazerunner.components.base import NAOAdapter
from .. import components, utils
from ..constants import STATES

logger = logging.getLogger('mazerunner')


class Agent(object):
    """Agent Base."""

    def __init__(self):
        self.cycle_ = 0

    def update(self):
        self.perceive()
        self.act()
        self.cycle_ += 1

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

    :param link:
        A link to V-REP, usually created by the `Environment` and shared
        throughout all the components. This can be overridden during the
        `start` procedure.

    :param random_state: RandomState-like, default=None.
        A random state used to control randomness in which the RoboticAgent
        acts. If None is passed, a new one is build with the current timestamp
        as seed.

    """

    STRIDE = 1.0
    SPEED = .7

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 random_state=None):
        if len(interface) != 2:
            raise ValueError('Invalid interface: %s' % str(interface))

        super(RoboticAgent, self).__init__()

        self.identity = identity
        self.interface = interface
        self.random_state = random_state or np.random.RandomState()

        self.motion = ALProxy("ALMotion", *interface)
        self.posture = ALProxy("ALRobotPosture", *interface)

        self.adapter = NAOAdapter(link, 'NAO') if link else None
        self.sensors = dict()

        self.joint_manager_ = None
        self.percept_ = None
        self.state_ = STATES.disabled

    def start(self, link=None):
        if link is not None:
            self.adapter = NAOAdapter(link, 'NAO')

        link = self.adapter.link

        self.motion.wakeUp()
        self.posture.goToPosture('Stand', self.SPEED)

        self.joint_manager_ = utils.JointManager(link=link,
                                                 motion=self.motion,
                                                 identity=self.identity,
                                                 robot_adapter=self.adapter)
        self.joint_manager_.start()

        self.sensors = {
            'vision': [
                components.Camera(link, component='NAO_vision1'),
                components.Camera(link, component='NAO_vision2'),
            ],
            'proximity': [
                # front
                components.ProximitySensor(link, component='Proximity_sensor1'),
                # back
                components.ProximitySensor(link, component='Proximity_sensor4'),
                # clockwise
                components.ProximitySensor(link, component='Proximity_sensor3'),
                # counter-clockwise
                components.ProximitySensor(link, component='Proximity_sensor2')
            ],
            'position': [
                components.Tag(link, component='tag1'),
                components.Tag(link, component='tag2'),
                components.Tag(link, component='tag3')
            ]
        }

        self.state_ = STATES.idle

    def perceive(self):
        # Get starting point, goal and robot positions. Then maps those to
        # numpy arrays first so norm and subtraction work properly.
        start, goal, me = (s.read().position for s in self.sensors['position'])

        # Assemble perceived state structure.
        self.percept_ = ([np.linalg.norm(goal - me)] +
                         [s.read().distance
                          for s in self.sensors['proximity']])
        return self

    def act(self):
        """Find a method with the same name of its current state and execute
        it.
        """
        return getattr(self, str(self.state_))()

    def stuck(self):
        """Reset agent to the starting point."""
        logger.info('agent is stuck. Restarting...')
        self.dispose().start(self.adapter.link)

    def dead(self):
        """Doesn't do anything."""
        logger.warning('attempt to update a dead agent')

    def dispose(self):
        self.motion.stopMove()
        self.posture.goToPosture('Stand', self.SPEED)

        # Stop sync routine.
        self.joint_manager_.dispose().join()

        # Clear adapter.
        self.adapter.dispose()

        self.state_ = STATES.dead
        self.cycle_ = 0

        return self
