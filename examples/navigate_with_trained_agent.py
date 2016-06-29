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
from mazerunner import agents, learning, utils

logging.basicConfig()
logger = logging.getLogger('mazerunner')
logger.setLevel(logging.DEBUG)

INTERFACE = ('127.0.0.1', 5000)
UPDATE_PERIOD = 0.5
ITERATIONS = None

if __name__ == "__main__":
    print(__doc__)

    # Load saved Q tabled.
    Q = utils.ModelStorage.load('snapshot.navigation.gz')

    # Rebuild model.
    model = learning.QLearning(alpha=0.2, gamma=.75, strategy='e-greedy',
                               epsilon=.85, Q=Q, checkpoint=10,
                               saving_name='snapshot.navigation.gz')

    agent = agents.Navigator(0, interface=INTERFACE, learning_model=model)

    mazerunner.Environment(agents=[agent], update_period=UPDATE_PERIOD,
                           life_cycles=ITERATIONS).live()

    print('Bye.')
