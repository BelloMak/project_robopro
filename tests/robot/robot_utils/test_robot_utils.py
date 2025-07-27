import numpy as np
import pytest

from roboter.common.error.custom_error import Error
from roboter.robot.robot_utils.robot_utils import (
    get_coordinates_transform_matrix,
    get_dh_transform_matrix,
    get_euler_angles_from_matrix,
    get_position_from_matrix,
)

MATRIX_TYPE = np.float64


@pytest.mark.parametrize(
    "a,d,alpha,theta,expected",
    [
        pytest.param(
            0,
            0,
            0,
            0,
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when zero input",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            0,
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 0, -1, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is zero first case",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            np.pi / 2,
            np.array(
                [
                    [0, 0, 1, 0],
                    [1, 0, 0, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 90 first case",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            np.pi,
            np.array(
                [
                    [-1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 180 first case",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            np.pi / 6,
            np.array(
                [
                    [0.866, 0, 0.5, 0],
                    [0.5, 0, -0.866, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 30 first case",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            np.pi / 4,
            np.array(
                [
                    [0.707, 0, 0.707, 0],
                    [0.707, 0, -0.707, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 45 first case",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            np.radians(55),
            np.array(
                [
                    [0.574, 0, 0.819, 0],
                    [0.819, 0, -0.574, 0],
                    [0, 1, 0, 0.21],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 55 first case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            0,
            np.array(
                [
                    [1, 0, 0, 0.12],
                    [0, 0.5, -0.866, 0],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is zero second case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            np.pi / 2,
            np.array(
                [
                    [0, -0.5, 0.866, 0],
                    [1, 0, 0, 0.12],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 90 second case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            np.pi,
            np.array(
                [
                    [-1, 0, 0, -0.12],
                    [0, -0.5, 0.866, 0],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 180 second case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            np.pi / 6,
            np.array(
                [
                    [0.866, -0.25, 0.433, 0.104],
                    [0.5, 0.433, -0.75, 0.06],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 30 second case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            np.pi / 4,
            np.array(
                [
                    [0.707, -0.354, 0.612, 0.085],
                    [0.707, 0.354, -0.612, 0.085],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 45 second case",
        ),
        pytest.param(
            0.12,
            0.35,
            np.pi / 3,
            np.radians(55),
            np.array(
                [
                    [0.574, -0.409, 0.709, 0.069],
                    [0.819, 0.287, -0.497, 0.098],
                    [0, 0.866, 0.5, 0.35],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when theta is 55 second case",
        ),
    ],
)
def test_get_dh_transform_matrix(a, d, alpha, theta, expected):
    matrix = get_dh_transform_matrix(a, d, alpha, theta)
    assert np.allclose(matrix, expected, atol=0.01)


@pytest.mark.parametrize(
    "x,y,z,alpha,beta,gamma,expected",
    [
        pytest.param(
            0,
            0,
            0,
            0,
            0,
            0,
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when zero input",
        ),
        pytest.param(
            0,
            0,
            0,
            np.pi / 2,
            0,
            0,
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 0, -1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 90 around x",
        ),
        pytest.param(
            0,
            0,
            0,
            0,
            np.pi / 2,
            0,
            np.array(
                [
                    [0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [-1, 0, 0, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 90 around y",
        ),
        pytest.param(
            0,
            0,
            0,
            0,
            0,
            np.pi / 2,
            np.array(
                [
                    [0, -1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 90 around z",
        ),
        pytest.param(
            0,
            0,
            0,
            np.pi / 6,
            0,
            0,
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 0.866, -0.5, 0],
                    [0, 0.5, 0.866, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 30 around x",
        ),
        pytest.param(
            0,
            0,
            0,
            0,
            np.pi / 6,
            0,
            np.array(
                [
                    [0.866, 0, 0.5, 0],
                    [0, 1, 0, 0],
                    [-0.5, 0, 0.866, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 30 around y",
        ),
        pytest.param(
            0,
            0,
            0,
            0,
            0,
            np.pi / 6,
            np.array(
                [
                    [0.866, -0.5, 0, 0],
                    [0.5, 0.866, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 30 around z",
        ),
        pytest.param(
            1,
            2,
            3,
            0,
            0,
            np.pi / 6,
            np.array(
                [
                    [0.866, -0.5, 0, 1],
                    [0.5, 0.866, 0, 2],
                    [0, 0, 1, 3],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate 30 around z and translate",
        ),
        pytest.param(
            3,
            2,
            1,
            np.pi / 6,
            np.pi / 4,
            np.pi / 3,
            np.array(
                [
                    [0.353, -0.612, 0.707, 3],
                    [0.926, 0.126, -0.353, 2],
                    [0.126, 0.780, 0.612, 1],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            id="success when rotate and translate all coordinates",
        ),
    ],
)
def test_get_coordinates_transform_matrix(
    x, y, z, alpha, beta, gamma, expected
):
    matrix = get_coordinates_transform_matrix(x, y, z, alpha, beta, gamma)
    assert np.allclose(matrix, expected, atol=0.01)


@pytest.mark.parametrize(
    "matrix,expected",
    [
        pytest.param(
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0, 0, 0), None),
            id="success when zero input",
        ),
        pytest.param(
            np.array(
                [
                    [0.353, -0.612, 0.707, 3],
                    [0.926, 0.126, -0.353, 2],
                    [0.126, 0.780, 0.612, 1],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((3, 2, 1), None),
            id="success when non zero input case 1",
        ),
        pytest.param(
            np.array(
                [
                    [0.866, -0.5, 0, 0],
                    [0.5, 0.866, 0, 1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0, 1, 0), None),
            id="success when non zero input case 2",
        ),
        pytest.param(
            np.array(
                [
                    [0.866, -0.5, 0, 0],
                    [0.5, 0.866, 0, 1],
                    [0, 0, 1, 0],
                ],
                dtype=MATRIX_TYPE,
            ),
            (None, Error()),
            id="error because wrong matrix size case 1",
        ),
        pytest.param(
            np.array(
                [
                    [0.866, -0.5, 0],
                    [0.5, 0.866, 0],
                    [0, 0, 1],
                    [0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            (None, Error()),
            id="error because wrong matrix size case 2",
        ),
    ],
)
def test_get_position_from_matrix(matrix, expected):
    expected_pos, expected_err = expected
    position, err = get_position_from_matrix(matrix)
    assert isinstance(err, type(expected_err))
    if position is not None:
        flag = True
        for a, b in zip(position, expected_pos):
            flag = flag * np.abs(a - b) < 0.01
        assert bool(flag) is True


@pytest.mark.parametrize(
    "matrix,expected",
    [
        pytest.param(
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0, 0, 0), None),
            id="success when zero input",
        ),
        pytest.param(
            np.array(
                [
                    [1, 0, 0, 3],
                    [0, 0, -1, 2],
                    [0, 1, 0, 1],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((np.pi / 2, 0, 0), None),
            id="success when rotate around x",
        ),
        pytest.param(
            np.array(
                [
                    [0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [-1, 0, 0, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0, np.pi / 2, 0), None),
            id="success when rotate around y",
        ),
        pytest.param(
            np.array(
                [
                    [0, -1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0, 0, np.pi / 2), None),
            id="success when rotate around z",
        ),
        pytest.param(
            np.array(
                [
                    [0.353, -0.612, 0.707, 0],
                    [0.926, 0.126, -0.353, 0],
                    [0.127, 0.780, 0.612, 0],
                    [0, 0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            ((0.905, -0.127, 1.206), None),
            id="success when rotate around all",
        ),
        pytest.param(
            np.array(
                [
                    [0.866, -0.5, 0, 0],
                    [0.5, 0.866, 0, 1],
                    [0, 0, 1, 0],
                ],
                dtype=MATRIX_TYPE,
            ),
            (None, Error()),
            id="error because wrong matrix size case 1",
        ),
        pytest.param(
            np.array(
                [
                    [0.866, -0.5, 0],
                    [0.5, 0.866, 0],
                    [0, 0, 1],
                    [0, 0, 1],
                ],
                dtype=MATRIX_TYPE,
            ),
            (None, Error()),
            id="error because wrong matrix size case 2",
        ),
    ],
)
def test_get_euler_angles_from_matrix(matrix, expected):
    expected_pos, expected_err = expected
    position, err = get_euler_angles_from_matrix(matrix)
    assert isinstance(err, type(expected_err))
    if position is not None:
        flag = True
        for a, b in zip(position, expected_pos):
            flag = flag and (np.abs(a - b) < 0.01)
        assert bool(flag) is True
