"""MazeRunner Navigator Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import time
from threading import Thread

from enum import Enum

from .base import RoboticAgent

States = Enum('disabled', 'idle', 'moving', 'dead')


class Navigator(RoboticAgent):
    """Navigator Agent."""

    speed = 1

    def __init__(self, robot_ip, robot_port):
        RoboticAgent.__init__(self, robot_ip, robot_port)

        self.state_ = States.disabled
        self.act_routine_ = None

    def perceive(self):
        return self

    def act(self):
        if self.state_ == States.disabled:
            self.motion.wakeUp()
            self.posture.goToPosture('StandInt', .5)

            self.state_ = States.idle

        elif self.state_ == States.idle:
            self.act_routine_ = Thread(target=self._move_routine)
            self.act_routine_.start()

        elif self.state_ == States.moving:
            pass

        return self

    def _move_routine(self):
        self.state_ = States.moving
        self.motion.moveToward(self.speed, 0, 0)

        while self.state_ == States.moving:
            time.sleep(4)

        self.motion.stopMove()
        self.motion.rest()

    def dispose(self):
        self.state_ = States.dead

        if self.act_routine_:
            self.act_routine_.join()
            self.act_routine_ = None
