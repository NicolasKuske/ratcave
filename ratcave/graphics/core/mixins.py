__author__ = 'nickdg'

import numpy as np
from . import _transformations as transformations
from collections import namedtuple

Color = namedtuple('Color', 'r g b a')

class Physical(object):


    def __init__(self, position=(0., 0., 0.), rotation=(0., 0., 0.), scale=1.):
        """XYZ Position, Scale and XYZEuler Rotation Class.

        Args:
            position (NumPy Array): (x, y, z) translation values.
            rotation (NNumPy Array): (x, y, z) rotation values
            scale (float): uniform scale factor. 1 = no scaling.
        """
        self.__position = np.array(position)
        self.rotation = np.array(rotation)
        self.scale = scale

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        assert len(value) == 3, "position must have three (x,y,z) coordinates."
        self.__position = np.array(value, dtype=float)

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        assert len(value) == 3, "rotation must have three (x,y,z) coordinates or be a 3x3 rotation matrix"
        if isinstance(value[0], (float, int)):
            self.__rotation = np.array(value, dtype=float)
        else:
            assert value.shape == (3,3), "rotation matrix must be a 3x3 numpy array"
            self.__rotation = value


    @property
    def model_matrix(self):
        """The 4x4 model matrix."""

        # Set Model and Normal Matrices
        trans_mat = transformations.translation_matrix(self.position)

        if self.__rotation.ndim == 1:
            rot_x_mat = transformations.rotation_matrix(np.radians(self.rotation[0]), [1, 0, 0])
            rot_y_mat = transformations.rotation_matrix(np.radians(self.rotation[1]), [0, 1, 0])
            rot_z_mat = transformations.rotation_matrix(np.radians(self.rotation[2]), [0, 0, 1])
            rot_mat = np.dot(np.dot(rot_z_mat,rot_y_mat), rot_x_mat)
        else:
            rot_mat = self.__rotation

        scale_mat = transformations.scale_matrix(self.scale)

        return np.dot(np.dot(trans_mat, rot_mat), scale_mat)

    @property
    def normal_matrix(self):
        """The 4x4 normal matrix, which is the inverse of the transpose of the model matrix."""
        return np.linalg.inv(self.model_matrix.T)

    @property
    def view_matrix(self):
        """The 4x4 view matrix."""
        # Set View Matrix
        trans_mat = transformations.translation_matrix(-self.position)

        if self.__rotation.ndim == 1:
            rot_x_mat = transformations.rotation_matrix(np.radians(-self.rotation[0]), [1, 0, 0])
            rot_y_mat = transformations.rotation_matrix(np.radians(-self.rotation[1]), [0, 1, 0])
            rot_z_mat = transformations.rotation_matrix(np.radians(-self.rotation[2]), [0, 0, 1])
            rot_mat = np.dot(np.dot(rot_x_mat, rot_y_mat), rot_z_mat)
        else:
            rot_mat = np.eye(4)
            rot_mat[:3, :3] = self.__rotation

        try:
            return np.dot(rot_mat, trans_mat)
        except:
            import pdb
            pdb.set_trace()

