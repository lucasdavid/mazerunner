"""Environment.

Execution manager for agents' periodic perception and action, controlling
frequency and iteration count.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging
import time

from .utils import vrep

logger = logging.getLogger('mazerunner')


class Environment:
    """Environment.

    Execution manager for agents' periodic perception and action, controlling
    frequency and iteration count.

    :param agents: list, default=()
        List of agents that compose this environment. If None is passed,
        assume that they will be inserted afterwards.

    :param update_period: float, default=.1
        Period to update on life cycle. The default behavior is to update
        every 100 milliseconds.

    :param life_cycles: int, default=None
        Maximum life cycles in which the environment will be alive. If None,
        no limit is imposed and environment will live eternally or until a
        `StopIteration` is raised.
    """

    def __init__(self, agents=(), update_period=.1, life_cycles=None):
        self.agents = agents
        self.update_period = update_period
        self.life_cycles = life_cycles

        self.tags_ = dict()

        self.cycle_ = -1
        self.link_ = None

    @property
    def is_alive(self):
        """Check whether this environment is alive or not.

        "Being alive" means that it has

        :return: True, if it is. False otherwise.
        """
        return self.cycle_ > -1 and (self.life_cycles is None or
                                     self.cycle_ < self.life_cycles)

    def live(self):
        """Makes This Environment Alive."""
        if self.is_alive:
            logging.error('Attempted to start an already '
                          'alive environment\'s life.')
            return self

        logger.info('Environment will live for %s iterations!',
                    str(self.life_cycles or 'infinite'))

        self.cycle_ = 0
        self._initialize()

        try:
            while self.is_alive:
                for agent in self.agents:
                    agent.update()

                time.sleep(self.update_period)
                logger.info('Iteration #%i finished.', self.cycle_)
                self.cycle_ += 1

        except KeyboardInterrupt:
            logger.info('Environment\'s life was interrupted by the user.')
        except StopIteration:
            logger.info('Environment\'s life ended naturally.')
        finally:
            self.dispose()

        return self

    def _initialize(self):
        logger.info('establishing link between V-REP and NAO...')

        vrep.simxFinish(-1)
        self.link_ = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

        assert self.link_ != -1, 'Could not connect to V-REP API.'

        for agent in self.agents:
            agent.start(self.link_)

        logger.info('link established')

    def dispose(self):
        for agent in self.agents:
            agent.dispose()

        vrep.simxFinish(-1)
