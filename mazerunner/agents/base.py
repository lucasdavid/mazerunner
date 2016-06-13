"""Agent Base.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
from naoqi import ALProxy


class Agent:
    """Agent Base."""

    def __init__(self, robot_ip, robot_port):
        # Init proxies.
        self.motion_proxy = ALProxy("ALMotion", robot_ip, robot_port)
        self.posture_proxy = ALProxy("ALRobotPosture", robot_ip, robot_port)

        self.busy_ = False

    def perceive(self):
        raise NotImplementedError

    def act(self):
        raise NotImplementedError
