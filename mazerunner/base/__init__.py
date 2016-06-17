"""Maze Runner Base.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class IUpdatable(object):
    """Updatable Interface.

    IUpdatable sub-classes are periodically updated by the environment.
    """

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError


@six.add_metaclass(abc.ABCMeta)
class IDisposable(object):
    """Disposable Interface.

    IDisposable sub-classes have more complicated disposal procedures, which
    must be explicitly called. For example, `RoboticAgents` need to join
    their action routines and send a "stop-moving" instruction to the robot.
    """

    @abc.abstractmethod
    def dispose(self):
        raise NotImplementedError
