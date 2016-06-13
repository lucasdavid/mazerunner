"""MazeRunner Utils.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import logging

logging.basicConfig()

logger = logging.getLogger('mazerunner')


def live(env, agents=None, iterations=100):
    """Makes an environment alive.

    :param env: Environment-like, the environment that should live.
    :param agents: optional, agents to place in the environment.
    :param iterations: int, number of iterations the environment will live.
    """
    it = 0

    if agents:
        if not hasattr(agents, '__iter__'): agents = [agents]
        env.agents += list(agents)

    logger.info('Environment will live for %i iterations!', iterations)

    while it < iterations:
        logger.info('#%i', it)
        env.update()

        it += 1

    logger.info('Environment\'s life has ended.')
