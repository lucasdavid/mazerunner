"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import time
from threading import Thread

import motion

from . import base, utils


class Walker(base.Agent):
    """Walker Agent."""

    def __init__(self, robot_ip, robot_port):
        base.Agent.__init__(self, robot_ip, robot_port)
        self.action_job_ = None

    def perceive(self):
        return self

    def act(self):
        if not self.busy_:
            self.action_job_ = Thread(target=self.routine)
            self.action_job_.start()

        return self

    def routine(self):
        self.busy_ = True
        utils.stiffness_on(self.motion_proxy)
        self.posture_proxy.goToPosture("StandInit", 0.5)
        self.motion_proxy.setWalkArmsEnabled(True, True)
        self.motion_proxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",
                                            True]])
        X = -0.5
        Y = 0.0
        Theta = 0.0
        Frequency = 0.0
        self.motion_proxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

        time.sleep(4.0)

        # TARGET VELOCITY
        X = 0.8
        Y = 0.0
        Theta = 0.0
        Frequency = 1.0  # max speed
        self.motion_proxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

        time.sleep(4.0)

        # TARGET VELOCITY
        X = 0.2
        Y = -0.5
        Theta = 0.2
        Frequency = 1.0
        self.motion_proxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

        time.sleep(2.0)

        #####################
        ## Arms User Motion
        #####################
        # Arms motion from user have always the priority than walk arms motion
        JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw",
                      "LElbowRoll"]
        Arm1 = [-40, 25, 0, -40]
        Arm1 = [x * motion.TO_RAD for x in Arm1]

        Arm2 = [-40, 50, 0, -80]
        Arm2 = [x * motion.TO_RAD for x in Arm2]

        pFractionMaxSpeed = 0.6

        self.motion_proxy.angleInterpolationWithSpeed(JointNames, Arm1,
                                                      pFractionMaxSpeed)
        self.motion_proxy.angleInterpolationWithSpeed(JointNames, Arm2,
                                                      pFractionMaxSpeed)
        self.motion_proxy.angleInterpolationWithSpeed(JointNames, Arm1,
                                                      pFractionMaxSpeed)

        time.sleep(2.0)

        #####################
        ## End Walk
        #####################
        # TARGET VELOCITY
        X = 0.0
        Y = 0.0
        Theta = 0.0
        self.motion_proxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

        self.busy_ = False
