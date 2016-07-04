"""Q-learning State.

Describes a state used by a Q-learning model.

Authors: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""


class State(object):
    """State Base Class.

    Describes a state used by a Q-learning model. This is a base class, and
    it must be overridden before used.

    """

    def __init__(self, data):
        self.data = data

    def reward(self, a, s1):
        raise NotImplementedError

    def discretize(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.data)

    def __hash__(self):
        return hash(str(self))
