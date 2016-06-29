"""QLearning Execution.

Exemplifies the usage of QLearning.

Author: Karina Bogdan  -- <karina.bogdan@gmail.com>

"""
from mazerunner.learning import QLearning

toy_state = [2.0, 0.6, 0.5, 0.4, 0.4]


def main():
    learner = QLearning()
    print(learner.IMMEDIATE_REWARD['collision'])

    for i in range(5):
        action = learner.update(percept=toy_state)
        print('action=', action)

        toy_state[1] -= 0.1
        toy_state[0] -= 0.1


if __name__ == '__main__':
    main()
