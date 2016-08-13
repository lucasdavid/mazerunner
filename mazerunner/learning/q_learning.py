"""Q-learning Algorithm.

Authors:
    Agnaldo     -- <agnaldo.esmael@ic.unicamp.br>
    Karina      -- <karina.bogdan@gmail.com>
    Lucas David -- <ld492@drexel.edu>


License: MIT (c) 2016

"""
import logging

import numpy as np
from enum import EnumValue

from .. import utils

logger = logging.getLogger('mazerunner')


class QLearning(object):
    """Q-learning.

    Generic Q-learning algorithm for multiple problems.

    :param actions: iterable
        Enumeration, list or tuple containing all possible actions
        for the agent which contains QLearning model.

    :param alpha: float, default=.1
        Learning rate of the algorithm.

    :param gamma: float, default=.75
        Discount factor.

    :param starting_epsilon: float, default=.5
        Probability of randomly selecting a action instead of the default
        `argmax Q[state]`. Decreases over time if n_epochs is passed, otherwise
        it's considered in its fullest (although you should consider passing
        0, if it's a trained execution).

    :param checkpoint: int, default=None
        If an integer, it will save a snapshot of the current model
        (the table Q) every `checkpoint` iterations.

    :param saving_name: str, default='snapshot.model.gz'
        File name used to save the model's snapshot. Used when persisting
        multiple models (E.g.: training multiple agents).

    :param random_state: RandomState-like
        Used to control the randomness of QLearning objects.

    """

    class QTable(object):
        """QTable.

        Abstraction for a sparse transition table for the Q-learning
        algorithm.

        """

        def __init__(self, actions, random_state=None):
            self.actions = actions
            self.random_state = random_state or np.random.RandomState()

            self.table_ = {}

        def at(self, state, action=None):
            """Get the transition value(es) for a given state.

            If no entry is found on the table, random transition values are
            created and inserted into the map on the fly, and finally returned.

            :param state: the state that's been looked for.
            :param action: Enum-object, int, default=None.
                An action associated to the returned value.
                If None is passed, all values (associated with every
                possible action) are returned.
            :return: list or float. The transition value(es).
            """
            state = str(state.discretize())

            if state not in self.table_:
                n_actions = len(self.actions)
                self.table_[state] = self.random_state.rand(n_actions).tolist()

            if isinstance(action, EnumValue):
                action = action.index

            weights = self.table_[state]
            return weights if action is None else weights[action]

        def __getitem__(self, item):
            """Shortcut to `at()` method.

            :param item: state or tuple (state, action)
            :return: list or float. Transition value(es).

            Examples:
            >>> q_table = QLearning.QTable()
            >>> state, action = State(), 3
            >>> q_table[state]
            >>> [20, 32, 32, 42]
            >>> q_table[state, action]
            >>> 42

            """
            if not isinstance(item, (list, tuple)):
                item = (item,)

            return self.at(*item)

        def set(self, state, action, value):
            """Set a transition value in the table.

            :param state: State-object. The row of interest.
            :param action: Enum-object, int. The column of interest.
            :param value: float. The value which should be set.
            :return: self
            """
            weights = self.at(state)

            if isinstance(action, EnumValue):
                action = action.index

            weights[action] = value

            return self

    def __init__(self, actions, alpha=0.1, gamma=0.75, starting_epsilon=.5,
                 n_epochs=0, checkpoint=None, saving_name='snapshot.model.gz',
                 random_state=None):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.starting_epsilon = starting_epsilon
        self.n_epochs = n_epochs
        self.checkpoint = checkpoint
        self.saving_name = saving_name
        self.random_state = random_state or np.random.RandomState()

        self.Q_ = QLearning.QTable(actions=actions,
                                   random_state=self.random_state)
        self.action_ = actions[0]
        self.state_ = None
        self.cycle_ = 0
        self.epoch_ = 0
        self.epsilon_ = None

    def start(self, state):
        self.state_ = state

        dw = (1 - self.epoch_ / self.n_epochs) if self.n_epochs else 1
        self.epsilon_ = (dw * self.starting_epsilon)

        return self

    def dispose(self):
        self.action_ = self.actions[0]
        self.state_ = None
        self.cycle_ = 0
        self.epoch_ = 0
        self.epsilon_ = None

        self.epoch_ += 1

    def update(self, state):
        """Update the table Q after the execution of the current action,
        which produced a new perception of the environment. Finally, find
        which action should be executed next.

        :param state: array-like, the current perception of the environment.
        """
        Q, s0, a0 = self.Q_, self.state_, self.action_

        # Update transition graph.
        Q.set(s0, a0, ((1 - self.alpha) * Q[s0, a0] +
                       self.alpha * (s0.reward(a0, state) +
                                     self.gamma * np.max(Q[state]))))
        self.state_ = state

        # Select next action.
        if self.random_state.rand() > self.epsilon_:
            action_code = np.argmax(Q[state])
            self.action_ = self.actions[action_code]
        else:
            self.action_ = self.random_state.choice(self.actions)

            logger.info('action %i was randomly chosen (e=%.2f)',
                        self.action_.index, self.epsilon_)

        if self.checkpoint and self.cycle_ % self.checkpoint == 0:
            logger.info('saving snapshot of Q-learning model...')
            utils.ModelStorage.save(Q.table_, path=self.saving_name)

        logger.info('[%i]\n'
                    '\tepsilon: %.2f\n'
                    '\tactions: %s > %s\n'
                    '\tstates: %s > %s\n'
                    '\tQ table: %s > %s\n',
                    self.cycle_, self.epsilon_,
                    a0.key, self.action_.key,
                    s0.discretize(), state.discretize(),
                    [round(n, 3) for n in Q[s0]],
                    [round(n, 3) for n in Q[state]])

        self.cycle_ += 1
        return self

    @classmethod
    def load(cls, model='snapshot.model.json', *args, **kwargs):
        """Load a persisted model."""
        instance = cls(*args, **kwargs)
        instance.Q_.table_ = utils.ModelStorage.load(model, raise_errors=False)
        return instance
