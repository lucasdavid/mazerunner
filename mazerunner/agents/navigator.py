"""MazeRunner Navigator Agent.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

import numpy as np
from enum import Enum

from . import Walker
from .. import learning
from ..components import ProximitySensor

logger = logging.getLogger('mazerunner')

ACTIONS = Enum('forward', 'backward', 'left', 'right')


class NavigationState(learning.State):
    IMMEDIATE_REWARD = {
        ACTIONS.forward: 1,
        ACTIONS.backward: 1,
        ACTIONS.right: 1,
        ACTIONS.left: 1,
        'collision': -10,
        'position-delta': 5,
        'close-to-goal': 10,
    }

    def reward(self, a, s1):
        """Immediate Reward Function."""
        reward = 0
        s0, s1 = self.data, s1.data

        # rewards related to states
        if any(proximity < ProximitySensor.COLLISION_THRESHOLD
               for proximity in s0[1:]):
            reward += self.IMMEDIATE_REWARD['collision']

        reward += (np.sign(s0[0] - s1[0]) *
                   self.IMMEDIATE_REWARD['position-delta'])

        if s1[0] < s0[0]:
            reward_proximity = (self.IMMEDIATE_REWARD['close-to-goal'] *
                                (1 - self.data[0] / 28))
            reward += reward_proximity
            logger.info('distance: %.2f, reward-proximity: %.2f',
                        s0[0], reward_proximity)

        # rewards related to actions.
        reward += self.IMMEDIATE_REWARD[a]

        logger.info('reward: %.2f', reward)
        return reward

    def discretize(self):
        goal_distance = [int(round(2 * self.data[0]))]
        orientation = [int(round(8 * (np.pi + self.data[1][2]) / (2 * np.pi)))]
        sensor_values = [int(round(i)) for i in self.data[2:]]

        return NavigationState(goal_distance + orientation + sensor_values)


class Navigator(Walker):
    """Navigator Agent.

    Navigates through the environment using a QLearning model.

    :param identity: [str, int], default=''.
        Integer or string that identifies the robot that will be controlled.
        E.g.: 0, '', 'jogger' or 'kyle'.

    :param interface: tuple (str, int).
        Tuple indicating the IP and port of the robot that will be controlled.
        E.g.: ('127.0.0.1', 5000), ('localhost', 6223).

    :param link: v-rep link.

    :param learning_model: QLearning model. If none is passed, a new one
        will be created.

    :param random_state: RandomState-like. Used to control the randomness
        of the process.

    """

    STRIDE = 1
    SPEED = .7

    INSTRUCTIONS_MAP = {
        ACTIONS.forward: (STRIDE, 0, 0),
        ACTIONS.backward: (-STRIDE, 0, 0),
        ACTIONS.left: (0, 0, np.pi / 2),
        ACTIONS.right: (0, 0, -np.pi / 2),
    }

    def __init__(self, identity='', interface=('127.0.0.1', 5000), link=None,
                 learning_model=None, random_state=None):
        super(Navigator, self).__init__(identity, interface, link, random_state)

        self.learning_model = learning_model or learning.QLearning(
            actions=ACTIONS, checkpoint=10,
            saving_name='snapshot.navigation.json')

    def start(self, link=None):
        super(Navigator, self).start(link)

        self.perception_ = ([12.4] +
                            [[0, 0, 0]] +
                            4 * [1])
        self.learning_model.start(NavigationState(self.perception_))

        return self

    def perceive(self):
        super(Navigator, self).perceive()

        sensors = self.sensors

        start, goal, me = (s.position for s in sensors['position'])

        self.perception_ = ([np.linalg.norm(goal - me)] +
                            [s.orientation for s in sensors['orientation']] +
                            [s.distance for s in sensors['proximity']])
        return self

    def idle(self):
        """Update the QLearning table, retrieve an action and check for
        dead-ends."""
        state = NavigationState(self.perception_)
        action = self.learning_model.update(state).action_

        if (all(s.imminent_collision for s in self.sensors['proximity']) or
            self.sensors['orientation'][0].is_lying_on_the_ground):
            # There's nothing left to be done, only flag this is a dead-end
            # so it can be restarted.
            self.behavior_ = self.BEHAVIORS.stuck

        else:
            move_to = self.INSTRUCTIONS_MAP[action]

            if action < ACTIONS.left:
                # It's walking straight or backwards. Reduce step size if it's
                # going against a close obstacle.
                dx = self.sensors['proximity'][action.index].distance

                move_to = np.clip(move_to, -dx, dx).tolist()

            self.motion.post.moveTo(*move_to)
            self.behavior_ = self.BEHAVIORS.moving

        return self

    def moving(self):
        """Makes sure the robot completes its actions before requesting
        a new one to its QLearning model."""
        if not self.motion.moveIsActive():
            self.behavior_ = self.BEHAVIORS.idle

    def dispose(self):
        super(Navigator, self).dispose()
        self.learning_model.dispose()

        return self
