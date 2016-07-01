"""MazeRunner Settings.

Define basic settings used throughout the whole program.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import os

TRAINING = True

e = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(e, '..')

ROBOT_MODEL_FILE = os.path.join(BASE_FOLDER, 'vrep-elements', 'models',
                                'perceptive-nao.ttm')

HOME_FOLDER = os.path.expanduser('~')
DATA_FOLDER = os.path.join(HOME_FOLDER, '.mazerunner')
