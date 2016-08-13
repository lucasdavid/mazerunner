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

from mazerunner import Environment, agents, learning
from mazerunner.agents import navigator

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

MODEL_PARAMS = dict(actions=navigator.ACTIONS, alpha=0.2, gamma=.75,
                    starting_epsilon=.01, n_epochs=1)

AGENT_PARAMS = dict(
    interface=('127.0.0.1', 5000),
)

ENV_PARAMS = dict(
    update_period=1,
    life_cycles=3000
)

if __name__ == "__main__":
    print(__doc__)

    model = learning.QLearning.load('snapshot.navtraining.json',
                                    **MODEL_PARAMS)
    agent = agents.Navigator(0, learning_model=model, **AGENT_PARAMS)
    env = Environment(agents=[agent], **ENV_PARAMS)

    try:
        logger.info('trained navigation has started')
        env.start().live().dispose()

    except KeyboardInterrupt:
        logger.info('environment\'s life was interrupted by the user.')
    except StopIteration:
        logger.info('environment\'s life ended naturally.')
    finally:
        env.dispose()

    print('bye')
