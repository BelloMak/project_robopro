from typing import Any, Optional, Tuple

import yaml

from roboter.common.error.runtime_error import RunTimeError


class ConfigParser(object):
    @classmethod
    def parse(
        cls, filename: str
    ) -> Tuple[Optional[Any], Optional[RunTimeError]]:
        """
        Create struct from yaml config file.
        """
        try:
            with open(filename, "r") as file:
                return yaml.safe_load(file), None
        except Exception as e:
            return None, RunTimeError(f"Failed when parsing: {e}")
