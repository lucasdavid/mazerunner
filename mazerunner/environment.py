"""Environment.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import time


class Environment:
    def __init__(self, agents=None, update_rate=.1):
        self.agents = agents or []
        self.update_rate = update_rate

    def update(self):
        for agent in self.agents:
            agent.perceive()
            agent.act()

        time.sleep(self.update_rate)
