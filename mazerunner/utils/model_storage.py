"""Model Storage.

Util for learning model persistence.

Author: Lucas David -- <ld492@drexel.edu>
License: MIT (c) 2016

"""
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
    def save(model, name='snapshot.model.gz'):
        """Save a learning model to a file.

        :param model: array-like, the model that will be saved.
        :param name: str, the name under which the model will be saved.
                     If the name ends with a '.gz' sequence, then the model
                     is automatically compressed.
        """
        ModelStorage._prepare()

        np.savetxt(os.path.join(settings.DATA_FOLDER, name), model)

    @staticmethod
    def load(name='snapshop.model.gz'):
        """Load a persisted learning model from the file.

        :param name: str, the name of the file which contains the model.
                     A file of same name must exist under
                     `settings.DATA_FOLDER`.
        :return: array-like, the learning model.
        """
        ModelStorage._prepare()

        return np.loadtxt(os.path.join(settings.DATA_FOLDER, name))
