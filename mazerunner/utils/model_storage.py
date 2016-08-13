"""Model Storage.

Util for learning model persistence.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
import json

import numpy as np


class ModelStorage(object):
    """Model Storage.

    Save learning models (numpy arrays) to files, automatically creating
    the necessary MazeRunner path substructure.

    Example:
        >>> # Create a model and save it to a file.
        >>> Q = {23: [.4, .2, .4, .0]}
        >>> ModelStorage.save(Q)
        >>> Q2 = ModelStorage.load()
        >>> np.testing.assert_array_equal(Q, Q2)

    """

    @staticmethod
    def save(model, path='snapshot.model.json'):
        """Save a learning model to a file.

        :param model: array-like, the model that will be saved.
        :param path: str, the path (filename included) under which the model
         should be saved.
        """
        with open(path, 'w') as f:
            json.dump(model, f)

    @staticmethod
    def load(path='snapshot.model.json', raise_errors=True):
        """Load a persisted learning model from the file.

        :param path: str, the path of the file which contains the model.
         A file under the same path must exist.
        :param raise_errors: if True, raises an error when the model
         isn't found. Otherwise, simply returns an empty model.
        :return: array-like, the learning model.
        """
        try:
            with open(path) as f:
                return json.load(f)
        except:
            if not raise_errors:
                return {}
            raise
