#!/usr/bin/env python3
import argparse
import math
import sys
from typing import Optional, Tuple

from PyQt6.QtWidgets import QApplication

from roboter.common.configuration.config_parser import ConfigParser
from roboter.common.error.custom_error import Error
from roboter.common.logger.logger import configure_logger
from roboter.common.stream.udp_stream import UdpClientStream
from roboter.gui.app_controller import AppController
from roboter.gui.app_model import AppModel
from roboter.gui.app_view import AppView
from roboter.robot.interface.i_robot import IRobot
from roboter.robot.joint.revolute_joint import RevoluteJoint
from roboter.robot.message_data_structures.six_joints_robot_msg_struct_unpacker import (
    SixJointsRobotDataUnpacker,
)
from roboter.robot.robot import CoordinateSystemPosition, Robot
from roboter.robot_controller.robot_controller import RobotController

SOCKET = "socket"
IP = "ip"
PORT = "port"
IS_BLOCKING = "is_blocking"
RECEIVE_TIMEOUT = "receive_timeout"

ROBOT_JOINT_1 = "joint_1"
ROBOT_JOINT_2 = "joint_2"
ROBOT_JOINT_3 = "joint_3"
ROBOT_JOINT_4 = "joint_4"
ROBOT_JOINT_5 = "joint_5"
ROBOT_JOINT_6 = "joint_6"
JOINT_A = "a"
JOINT_D = "d"
JOINT_ALPHA = "alpha"
BASE_POSITION = "base_pos"
END_EFFECTOR_POSITION = "end_effector_pos"
X = "x"
Y = "y"
Z = "z"
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"

REQUIRED_ARGS = set(["config", "robot"])


def args_parse() -> Tuple[Optional[argparse.Namespace], Optional[Error]]:
    """
    Parse configuration from command line.
    """
    argparser = argparse.ArgumentParser(description="Robopro robot terminal")

    argparser.add_argument(
        "--config",
        metavar="C",
        default="./config/terminal_config.yaml",
        type=str,
        help="Path to the configuration file for terminal.",
    )

    argparser.add_argument(
        "--robot",
        metavar="R",
        default="./config/robot_config.yaml",
        type=str,
        help="Path to the configuration file for robot",
    )

    argparser.add_argument(
        "--logger",
        metavar="L",
        default="./config/logger_config.conf",
        type=str,
        help="Path to the configuration file for logger",
    )

    args, _ = argparser.parse_known_args()

    for required in REQUIRED_ARGS:
        if getattr(args, required) is None:
            return None, Error(f"Argument is missing: --{required}")

    return args, None


class RobotTerminalEntryPoint(object):
    def __init__(self, terminal_config, robot_config):
        self.robot_terminal_config = terminal_config
        self.robot_config = robot_config
        self.robot = None
        self.socket = None
        self.unpacker = None
        self.robot_controller = None
        self.app = None
        self.app_model = None
        self.app_controller = None
        self.app_view = None

    def start(self) -> Optional[Error]:
        # Define data stream
        self.socket = UdpClientStream(
            hostname=self.robot_terminal_config[SOCKET][IP],
            port=self.robot_terminal_config[SOCKET][PORT],
            is_blocking=self.robot_terminal_config[SOCKET][IS_BLOCKING],
            receive_timeout=self.robot_terminal_config[SOCKET][
                RECEIVE_TIMEOUT
            ],
        )
        self.unpacker = SixJointsRobotDataUnpacker()

        # Define robot controller
        self.robot, err = self._construct_robot()
        if err is not None or self.robot is None:
            return err
        self.robot_controller = RobotController(
            self.robot, self.socket, self.unpacker
        )

        # Define GUI
        self.app = QApplication(sys.argv)
        self.app_model = AppModel(self.robot_controller)
        self.app_view = AppView()
        self.app_controller = AppController(self.app_model, self.app_view)

        # Define GUI handlers
        self.app_view.on_get_robot_position_click(
            self.app_controller.handle_get_end_effector_position
        )
        self.app_view.on_clear_table_click(
            self.app_controller.handle_clear_table
        )

        self.app_view.show()

        sys.exit(self.app.exec())

    def _construct_robot(self) -> Tuple[Optional[IRobot], Optional[Error]]:
        """
        Construct robot from config
        """
        robot = Robot()

        err = robot.set_base_position(
            CoordinateSystemPosition(
                self.robot_config[BASE_POSITION][X],
                self.robot_config[BASE_POSITION][Y],
                self.robot_config[BASE_POSITION][Z],
                self.robot_config[BASE_POSITION][ALPHA],
                self.robot_config[BASE_POSITION][BETA],
                self.robot_config[BASE_POSITION][GAMMA],
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_1][JOINT_A],
                self.robot_config[ROBOT_JOINT_1][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_1][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_2][JOINT_A],
                self.robot_config[ROBOT_JOINT_2][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_2][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_3][JOINT_A],
                self.robot_config[ROBOT_JOINT_3][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_3][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_4][JOINT_A],
                self.robot_config[ROBOT_JOINT_4][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_4][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_5][JOINT_A],
                self.robot_config[ROBOT_JOINT_5][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_5][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.add_joint(
            RevoluteJoint(
                self.robot_config[ROBOT_JOINT_6][JOINT_A],
                self.robot_config[ROBOT_JOINT_6][JOINT_D],
                math.radians(self.robot_config[ROBOT_JOINT_6][JOINT_ALPHA]),
            )
        )
        if err is not None:
            return None, err

        err = robot.set_end_effector_pos(
            CoordinateSystemPosition(
                self.robot_config[END_EFFECTOR_POSITION][X],
                self.robot_config[END_EFFECTOR_POSITION][Y],
                self.robot_config[END_EFFECTOR_POSITION][Z],
                self.robot_config[END_EFFECTOR_POSITION][ALPHA],
                self.robot_config[END_EFFECTOR_POSITION][BETA],
                self.robot_config[END_EFFECTOR_POSITION][GAMMA],
            )
        )
        if err is not None:
            return None, err

        return robot, None


def main():
    entry_point = None
    args, err = args_parse()
    if err is not None or args is None:
        print(str(err))
        exit(1)
    configure_logger(args.logger, "main")
    robot_terminal_config, err = ConfigParser.parse(args.config)
    if err is not None or robot_terminal_config is None:
        print(str(err))
        exit(1)
    robot_config, err = ConfigParser.parse(args.robot)
    if err is not None or robot_config is None:
        print(str(err))
        exit(1)
    entry_point = RobotTerminalEntryPoint(robot_terminal_config, robot_config)
    err = entry_point.start()
    if err is not None:
        print(str(err))
        exit(1)


if __name__ == "__main__":
    main()
