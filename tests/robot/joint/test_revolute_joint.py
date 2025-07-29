import numpy as np
import pytest

from roboter.robot.joint.revolute_joint import RevoluteJoint

MATRIX_TYPE = np.float64


@pytest.mark.parametrize(
    "a,d,alpha,theta,expected",
    [
        pytest.param(
            0,
            0,
            0,
            0,
            (
                np.array(
                    [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ],
                    dtype=MATRIX_TYPE,
                ),
                None,
            ),
            id="success when zero input",
        ),
        pytest.param(
            0,
            0.21,
            np.pi / 2,
            0,
            (
                np.array(
                    [
                        [1, 0, 0, 0],
                        [0, 0, -1, 0],
                        [0, 1, 0, 0.21],
                        [0, 0, 0, 1],
                    ],
                    dtype=MATRIX_TYPE,
                ),
                None,
            ),
            id="success when non zero input case 1",
        ),
        pytest.param(
            5,
            2,
            np.pi / 4,
            np.pi / 6,
            (
                np.array(
                    [
                        [0.866, -0.354, 0.354, 4.33],
                        [0.5, 0.612, -0.612, 2.5],
                        [0, 0.707, 0.707, 2],
                        [0, 0, 0, 1],
                    ],
                    dtype=MATRIX_TYPE,
                ),
                None,
            ),
            id="success when non zero input case 2",
        ),
    ],
)
def test_get_matrix_for_first_joint_config(a, d, alpha, theta, expected):
    joint = RevoluteJoint(a, d, alpha)
    expected_matrix, expected_err = expected

    matrix, err = joint.get_matrix(theta)
    assert isinstance(err, type(expected_err))
    if matrix is not None:
        assert np.allclose(matrix, expected_matrix, atol=0.001)
