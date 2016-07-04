import numpy as np
import matplotlib.pyplot as plt

from mazerunner.utils import ModelStorage

MODEL_NAME = 'greedy.navigation.gz'


def main():
    Q = ModelStorage.load(MODEL_NAME)
    Q_ = (Q - Q.mean()) / (Q.max() - Q.min())

    fig, ax = plt.subplots()
    heatmap = ax.pcolor(Q_, cmap=plt.cm.YlOrBr, alpha=0.8)

    fig = plt.gcf()
    fig.set_size_inches(8, 8)
    ax.set_frame_on(False)

    ax.set_xticklabels([1, 2, 3, 4], minor=False)
    ax.grid(False)
    ax = plt.gca()

    fig.savefig('report.png')


if __name__ == '__main__':
    main()
