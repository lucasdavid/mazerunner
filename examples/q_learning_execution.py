from mazerunner.learning import QLearning

state = [2.0, 0.6, 0.5, 0.4, 0.4]


def main():
    learner = QLearning()
    print(learner.IMMEDIATE_REWARD['collision'])

    for i in range(5):
        action = learner.get_action()
        print('action=', action)

        state[1] -= 0.1
        state[0] -= 0.1

        learner.update(state)


if __name__ == '__main__':
    main()
