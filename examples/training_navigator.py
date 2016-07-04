"""Training Navigator Agent.

Train a Navigator Agent to walk through the house, looking for the kitchen.

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

# Training epochs.
N_EPOCHS = 100
SAVING_NAME = 'snapshot.navtraining.json'

MODEL_PARAMS = dict(
    actions=navigator.ACTIONS,
    alpha=0.2, gamma=.75, starting_epsilon=.85,
    n_epochs=N_EPOCHS,
    checkpoint=10, saving_name=SAVING_NAME,
)

AGENT_PARAMS = dict(
    interface=('127.0.0.1', 5000),
)

ENV_PARAMS = dict(
    update_period=1,
    life_cycles=1000
)

if __name__ == "__main__":
    print(__doc__)

    model = learning.QLearning.load(SAVING_NAME, **MODEL_PARAMS)
    agent = agents.Navigator(0, learning_model=model,
                             **AGENT_PARAMS)

    env = Environment(agents=[agent], **ENV_PARAMS)

    try:
        for epoch in range(N_EPOCHS):
            logger.info('epoch %i has started', epoch)
            (env
             .start()
             .live()
             .dispose())

    except KeyboardInterrupt:
        logger.info('Environment\'s life was interrupted by the user.')
    except StopIteration:
        logger.info('Environment\'s life ended naturally.')
    finally:
        env.dispose()

    print('Bye.')
