"""Navigate with Trained Agent.

Navigate through the house looking for the kitchen using a previously trained
Q-learning model.

Author:
    Agnaldo Esmael -- <agnaldo.esmael@ic.unicamp.br>
    Karina Bogdan  -- <karina.bogdan@gmail.com>
    Lucas David    -- <lucas.david@drexel.edu>
    Renan Baima    -- <renanbaima@gmail.com>

License: MIT (c) 2016

"""
import logging

import mazerunner
from mazerunner import agents, learning
from mazerunner.agents import navigator

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

INTERFACE = ('127.0.0.1', 5000)
UPDATE_PERIOD = 1
ITERATIONS = 1000

PARAMS = dict(
    alpha=.2, gamma=.75, epsilon=0,
    checkpoint=10, saving_name='snapshot.navigation.gz'
)

if __name__ == "__main__":
    print(__doc__)

    # Load a navigation model.
    model = learning.QLearning.load(actions=navigator.ACTIONS, **PARAMS)
    # Rebuild the agent.
    agent = agents.Navigator(0, interface=INTERFACE, learning_model=model)
    # Build the environment.
    env = mazerunner.Environment(agents=[agent], update_period=UPDATE_PERIOD,
                                 life_cycles=ITERATIONS)
    try:
        env.live()
    except KeyboardInterrupt:
        logger.info('Environment\'s life was interrupted by the user.')
    except StopIteration:
        logger.info('Environment\'s life ended naturally.')

    print('Bye.')
