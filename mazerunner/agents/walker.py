"""MazeRunner Walker Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import time
from threading import Thread

import motion

from . import base


class Walker(base.RoboticAgent):
    """Walker Agent."""

    def __init__(self, robot_ip, robot_port):
        base.RoboticAgent.__init__(self, robot_ip, robot_port)
        self.acting_ = False
        self.act_routine_ = None

    def perceive(self):
        return self

    def act(self):
        if not self.acting_:
            self.act_routine_ = Thread(target=self.routine)
            self.act_routine_.start()

        return self

    def routine(self):
        self.acting_ = True

        self.motion.wakeUp()
        self.posture.goToPosture('StandInt', .5)

        X = -0.5
        Y = 0.0
        Theta = 0.0
        Frequency = 0.0
        self.motion.setWalkTargetVelocity(X, Y, Theta, Frequency)

        time.sleep(4.0)

        # TARGET VELOCITY
        X = 0.8
        Y = 0.0
        Theta = 0.0
        Frequency = 1.0  # max speed
        self.motion.setWalkTargetVelocity(X, Y, Theta, Frequency)

        time.sleep(4.0)

        # TARGET VELOCITY
        X = 0.2
        Y = -0.5
        Theta = 0.2
        Frequency = 1.0
        self.motion.setWalkTargetVelocity(X, Y, Theta, Frequency)

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

        self.motion.angleInterpolationWithSpeed(JointNames, Arm1,
                                                pFractionMaxSpeed)
        self.motion.angleInterpolationWithSpeed(JointNames, Arm2,
                                                pFractionMaxSpeed)
        self.motion.angleInterpolationWithSpeed(JointNames, Arm1,
                                                pFractionMaxSpeed)

        time.sleep(2.0)

        self.motion.stopMove()
        self.motion.rest()

        self.acting_ = False

    def dispose(self):
        if self.act_routine_:
            self.act_routine_.join()
            self.act_routine_ = None
