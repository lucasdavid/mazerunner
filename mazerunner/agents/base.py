"""Agent Base.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import abc
import six

from naoqi import ALProxy

from ..base import IUpdatable, IDisposable


@six.add_metaclass(abc.ABCMeta)
class Agent(IUpdatable, IDisposable):
    """Agent Base."""

    def update(self):
        self.perceive()
        self.act()

    @abc.abstractmethod
    def perceive(self):
        raise NotImplementedError

    @abc.abstractmethod
    def act(self):
        raise NotImplementedError


@six.add_metaclass(abc.ABCMeta)
class RoboticAgent(Agent):
    """Robot Agent Base."""

    def __init__(self, robot_ip, robot_port):
        self.interface = robot_ip, robot_port

        self.motion = ALProxy("ALMotion", *self.interface)
        self.posture = ALProxy("ALRobotPosture", *self.interface)
        self.memory = ALProxy('ALMemory', *self.interface)
        self.sonar = ALProxy('ALSonar', *self.interface)
