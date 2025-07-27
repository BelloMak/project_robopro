from typing import Optional, Tuple

import numpy as np

from roboter.common.error.custom_error import Error
from roboter.common.error.data_type_error import DataTypeError
from roboter.robot.joint.interface.i_joint import Matrix


def get_coordinates_transform_matrix(
    x: float,
    y: float,
    z: float,
    alpha: float = 0,
    beta: float = 0,
    gamma: float = 0,
) -> Matrix:
    """
    Get transform matrix for specified coordinates.
    """
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    cb = np.cos(beta)
    sb = np.sin(beta)
    cg = np.cos(gamma)
    sg = np.sin(gamma)

    matrix = np.array(
        [
            [cb * cg, -sg * cb, sb, x],
            [sa * sb * cg + sg * ca, -sa * sb * sg + ca * cg, -sa * cb, y],
            [sa * sg - sb * ca * cg, sa * cg + sb * sg * ca, ca * cb, z],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )

    return matrix


def get_dh_transform_matrix(
    a: float, d: float, alpha: float, theta: float
) -> Matrix:
    """
    Get DH matrix for specified theta angle in radians.
    """

    matrix = np.array(
        [
            [
                np.cos(theta),
                -np.sin(theta) * np.cos(alpha),
                np.sin(theta) * np.sin(alpha),
                a * np.cos(theta),
            ],
            [
                np.sin(theta),
                np.cos(theta) * np.cos(alpha),
                -np.cos(theta) * np.sin(alpha),
                a * np.sin(theta),
            ],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )
    return matrix


def get_euler_angles_from_matrix(
    matrix: Matrix,
) -> Tuple[Optional[Tuple[float, float, float]], Optional[Error]]:
    """
    Get Euler ZYX angles from 4x4 coordinates transformation matrix.
    """

    a, b = matrix.shape
    if a != 4 or b != 4:
        return None, DataTypeError("wrong matrix size")
    r = matrix[2, 0]
    theta = -np.asin(r)
    if 1 - np.abs(r) < 0.01:
        phi = 0
        psi = np.atan2(matrix[0, 1], matrix[0, 2])
        return (psi, theta, phi), None

    denom = np.cos(theta)
    psi = np.atan2(matrix[2, 1] / denom, matrix[2, 2] / denom)
    phi = np.atan2(matrix[1, 0] / denom, matrix[0, 0] / denom)
    return (float(psi), float(theta), float(phi)), None


def get_position_from_matrix(
    matrix: Matrix,
) -> Tuple[Optional[Tuple[float, float, float]], Optional[Error]]:
    """
    Get position from 4x4 coordinates transformation matrix.
    """

    a, b = matrix.shape
    if a != 4 or b != 4:
        return None, DataTypeError("wrong matrix size")

    x, y, z = matrix[:3, 3]
    return (float(x), float(y), float(z)), None
