import socket
import time
from typing import Optional, Tuple

from roboter.common.error.connection_error import ConnectionError
from roboter.common.error.custom_error import Error
from roboter.common.error.runtime_error import RunTimeError
from roboter.common.logger.logger import debug
from roboter.common.stream.interface.i_stream import (
    IStream,
    ReceiveResult,
)


class UdpClientStream(IStream):
    def __init__(
        self,
        hostname: str,
        port: int,
        is_blocking: bool = False,
        buffer_size: int = 1024,
    ):
        self._hostname = hostname
        self._port = port
        self._is_blocking = is_blocking
        self._buffer_size = buffer_size
        self._socket = None
        self._is_open = False

    def open(self) -> Optional[Error]:
        """
        Open a UDP socket using host and port specified in class constructor.
        """

        if self._is_open:
            return RunTimeError("udp socket already opened")

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setblocking(self._is_blocking)
            self._is_open = True
            debug(f"Opened UDP socket on {self._hostname}:{self._port}")
            return None
        except socket.error as e:
            return ConnectionError(
                f"error occurred when opening udp socket on {self._hostname}:{self._port}: {e}"
            )

    def close(self) -> Optional[Error]:
        """
        Close the UDP socket.
        """

        if not self._is_open or self._socket is None:
            return RunTimeError("udp socket already closed")

        try:
            self._socket.close()
            debug(f"Closed UDP socket on {self._hostname}:{self._port}")
            self._is_open = False
            return None
        except socket.error as e:
            self._is_open = False
            return ConnectionError(
                f"error occurred when closing udp socket on {self._hostname}:{self._port}: {e}"
            )

    def send_data(self, data: bytes) -> Optional[Error]:
        """
        Send data to socket.
        """

        if not self._is_open or self._socket is None:
            return RunTimeError("failed to send data, udp socket closed")

        try:
            self._socket.sendto(data, (self._hostname, self._port))
            return None
        except Exception as e:
            return ConnectionError(
                f"error occurred when sending data via udp on {self._hostname}:{self._port}: {e}"
            )

    def receive_data(
        self, buffer_size: int = 0, timeout: int = 1
    ) -> Tuple[ReceiveResult, Optional[Error]]:
        """
        Read data from socket.
        """

        if not self._is_open or self._socket is None:
            return (None, False), ConnectionError(
                "connection is not established"
            )
        if buffer_size == 0:
            buffer_size = self._buffer_size

        start = time.time()
        while True:
            if time.time() - start > timeout:
                return (None, False), ConnectionError(
                    "timeout occurred when receiving data"
                )
            try:
                raw_data = self._socket.recv(buffer_size)
                has_received = len(raw_data) > 0
                error = None
                if has_received:
                    break
            except BlockingIOError:
                raw_data = None
                has_received = False
                error = None
            except socket.error as e:
                raw_data = None
                has_received = False
                error = ConnectionError(
                    f"error occurred when receiving data via udp on {self._hostname}:{self._port}: {e}"
                )
            time.sleep(0.01)
        return (raw_data, has_received), error

    def __del__(self):
        if self._is_open and self._socket is not None:
            self._socket.close()
        self._socket = None
