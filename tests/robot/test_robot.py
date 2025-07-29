from unittest.mock import MagicMock

import numpy as np
from pytest import fixture

from roboter.common.error.custom_error import Error
from roboter.robot.interface.i_robot import CoordinateSystemPosition
from roboter.robot.joint.interface.i_joint import IJoint
from roboter.robot.robot import Robot


@fixture
def robot():
    return Robot()


@fixture
def position():
    return CoordinateSystemPosition(1, 1, 1, 0, 0, 0)


@fixture
def joint():
    joint: IJoint = MagicMock()
    matrix = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )
    joint.get_matrix.return_value = (matrix, None)
    return joint


@fixture
def joint_with_error():
    joint: IJoint = MagicMock()
    joint.get_matrix.return_value = (None, Error("test_error"))
    return joint


def test_set_base_position(robot, position):
    err = robot.set_base_position(position)
    assert err is None


def test_set_end_effector_pos(robot, position):
    err = robot.set_end_effector_pos(position)
    assert err is None


def test_add_joint(robot, joint):
    err = robot.add_joint(joint)
    assert err is None
    err = robot.add_joint(joint)
    assert err is None


def test_get_ee_position_success_without_base_and_ee_config(robot, joint):
    expected_matrix = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )
    err = robot.add_joint(joint)
    assert err is None
    err = robot.add_joint(joint)
    assert err is None
    matrix, err = robot.get_ee_position((0, 0))
    assert err is None
    assert np.allclose(matrix, expected_matrix, atol=0.01)


def test_get_ee_position_success_with_base_and_ee_config(
    robot, joint, position
):
    expected_matrix = np.array(
        [
            [1, 0, 0, 2],
            [0, 1, 0, 2],
            [0, 0, 1, 2],
            [0, 0, 0, 1],
        ],
        dtype=np.float64,
    )
    err = robot.set_base_position(position)
    assert err is None
    err = robot.set_end_effector_pos(position)
    assert err is None
    err = robot.add_joint(joint)
    assert err is None
    err = robot.add_joint(joint)
    assert err is None
    matrix, err = robot.get_ee_position((0, 0))
    assert err is None
    assert np.allclose(matrix, expected_matrix, atol=0.01)


def test_get_ee_position_error_because_joint_get_matrix_failed(
    robot, joint_with_error, joint
):
    err = robot.add_joint(joint_with_error)
    assert err is None
    err = robot.add_joint(joint)
    assert err is None
    matrix, err = robot.get_ee_position((0, 0))
    assert isinstance(err, Error)
    assert matrix is None


def test_get_ee_position_error_because_wrong_number_of_joints_pos(
    robot, joint
):
    err = robot.add_joint(joint)
    assert err is None
    matrix, err = robot.get_ee_position((0, 0))
    assert isinstance(err, Error)
    assert matrix is None
