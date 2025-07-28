from unittest.mock import MagicMock

import numpy as np
from pytest import fixture

from roboter.common.error.custom_error import Error
from roboter.common.stream.interface.i_stream import IStream
from roboter.robot.interface.i_robot import IRobot
from roboter.robot.message_data_structures.interface.i_message_structure_unpacker import (
    IJointsDataUnpacker,
)
from roboter.robot_controller.robot_controller import RobotController


def create_stream(open_err, send_err, receive_data, receive_err) -> IStream:
    stream: IStream = MagicMock()
    stream.open.return_value = open_err
    stream.close.return_value = None
    stream.send_data.return_value = send_err
    stream.receive_data.return_value = (
        (receive_data, receive_data is not None),
        receive_err,
    )
    return stream


@fixture
def unpacker():
    unpacker: IJointsDataUnpacker = MagicMock()
    unpacker.unpack.return_value = (MagicMock(), None)
    unpacker.get_message_size.return_value = 10
    return unpacker


@fixture
def unpacker_with_error():
    unpacker: IJointsDataUnpacker = MagicMock()
    unpacker.unpack.return_value = (None, Error("unpack error"))
    unpacker.get_message_size.return_value = 10
    return unpacker


@fixture
def robot():
    robot: IRobot = MagicMock()
    robot.get_ee_position.return_value = (
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=np.float64,
        ),
        None,
    )
    return robot


@fixture
def robot_with_error():
    robot: IRobot = MagicMock()
    robot.get_ee_position.return_value = (
        None,
        Error("get position error"),
    )
    return robot


def test_get_robot_position_success(robot, unpacker):
    strean = create_stream(
        None,
        None,
        10,
        None,
    )
    controller = RobotController(robot, strean, unpacker)
    result, err = controller.get_robot_position()
    assert err is None
    assert result is not None


def test_get_robot_position_error_because_stream_open_failed(robot, unpacker):
    strean = create_stream(
        Error(),
        None,
        10,
        None,
    )
    controller = RobotController(robot, strean, unpacker)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None


def test_get_robot_position_error_because_stream_send_data_failed(
    robot, unpacker
):
    strean = create_stream(
        None,
        Error(),
        10,
        None,
    )
    controller = RobotController(robot, strean, unpacker)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None


def test_get_robot_position_error_because_stream_receive_data_failed(
    robot, unpacker
):
    strean = create_stream(
        None,
        None,
        10,
        Error(),
    )
    controller = RobotController(robot, strean, unpacker)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None


def test_get_robot_position_error_because_stream_receive_data_empty(
    robot, unpacker
):
    strean = create_stream(
        None,
        None,
        None,
        None,
    )
    controller = RobotController(robot, strean, unpacker)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None


def test_get_robot_position_error_because_msg_unpack_failed(
    robot, unpacker_with_error
):
    strean = create_stream(
        None,
        None,
        10,
        None,
    )
    controller = RobotController(robot, strean, unpacker_with_error)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None


def test_get_robot_position_error_because_robot_get_pos_failed(
    robot_with_error, unpacker
):
    strean = create_stream(
        None,
        None,
        10,
        None,
    )
    controller = RobotController(robot_with_error, strean, unpacker)
    result, err = controller.get_robot_position()
    assert isinstance(err, Error)
    assert result is None
