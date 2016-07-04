"""Model Storage.

Util for learning model persistence.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import json
import os

import numpy as np

from .. import settings


class ModelStorage(object):
    """Model Storage.

    Save learning models (numpy arrays) to files, automatically creating
    the necessary MazeRunner path substructure.

    Example:
        >>> # Create a model and save it to a file.
        >>> Q = np.random.rand(40, 40)
        >>> ModelStorage.save(Q)
        >>> Q2 = ModelStorage.load()
        >>> np.testing.assert_array_equal(Q, Q2)

    """

    @staticmethod
    def _prepare():
        """Check and create required folder structure."""
        if not os.path.exists(settings.DATA_FOLDER):
            os.mkdir(settings.DATA_FOLDER)

    @staticmethod
    def save(model, name='snapshot.model.json'):
        """Save a learning model to a file.

        :param model: array-like, the model that will be saved.
        :param name: str, the name under which the model will be saved.
        """
        ModelStorage._prepare()

        with open(os.path.join(settings.DATA_FOLDER, name), 'w') as f:
            json.dump(model, f)

    @staticmethod
    def load(name='snapshop.model.json', create_if_not_found=False):
        """Load a persisted learning model from the file.

        :param name: str, the name of the file which contains the model.
                     A file of same name must exist under
                     `settings.DATA_FOLDER`.
        :return: array-like, the learning model.
        """
        ModelStorage._prepare()

        try:
            with open(os.path.join(settings.DATA_FOLDER, name)) as f:
                return json.load(f)
        except:
            if create_if_not_found:
                return {}

            raise
