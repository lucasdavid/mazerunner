"""Agent Base.

Basic definitions, such as the Agent and RoboticAgent base classes.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import time
from enum import Enum
from naoqi import ALProxy

from ..utils import JointManager


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
        if len(interface) != 2:
            raise ValueError('Invalid interface: %s' % str(interface))

        self.identity = identity
        self.interface = interface

        self.motion = ALProxy("ALMotion", *interface)
        self.posture = ALProxy("ALRobotPosture", *interface)
        self.memory = ALProxy('ALMemory', *interface)
        self.sonar = ALProxy('ALSonar', *interface)

        self.true_identity_ = 'robot-' + str(identity)
        self.state_ = self.States.disabled

        self.link_ = None
        self.joint_manager_ = None

    def act(self):
        """Find a method with the same name of its current state and execute
        it.
        """
        return getattr(self, str(self.state_))()

    def start(self, link):
        self.link_ = link

        self.motion.wakeUp()
        self.posture.goToPosture('Stand', .5)

        self.joint_manager_ = JointManager(link=self.link_,
                                           motion=self.motion,
                                           identity=self.identity)
        self.joint_manager_.start()
        self.sonar.subscribe(self.true_identity_)

        self.state_ = self.States.idle

    def dispose(self):
        self.sonar.unsubscribe(self.true_identity_)
        self.motion.stopMove()
        self.motion.rest()

        # Stop sync routine.
        self.joint_manager_.active_ = False
        self.joint_manager_.join()

        self.state_ = self.States.dead

        return self
