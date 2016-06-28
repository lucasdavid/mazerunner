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
    def data_folder():
        return os.path.join(settings.BASE_FOLDER, settings.MODEL_FOLDER)

    @staticmethod
    def _prepare():
        if not os.path.exists(settings.BASE_FOLDER):
            os.mkdir(settings.BASE_FOLDER)

        folder = ModelStorage.data_folder()
        if not os.path.exists(folder):
            os.mkdir(folder)

        return ModelStorage

    @staticmethod
    def save(model, name='snapshot.model.gz'):
        folder = ModelStorage._prepare().data_folder()

        np.savetxt(os.path.join(folder, name), model)

    @staticmethod
    def load(name='snapshop.model.gz'):
        folder = ModelStorage._prepare().data_folder()

        return np.loadtxt(os.path.join(folder, name))
