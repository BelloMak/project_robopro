from abc import ABCMeta, abstractmethod
from typing import Optional, Tuple

import numpy as np
import numpy.typing as npt

from roboter.common.error.custom_error import Error

Matrix = npt.NDArray[np.float64]


class IJoint(object, metaclass=ABCMeta):
    @abstractmethod
    def get_matrix(
        self, variable_param: float
    ) -> Tuple[Optional[Matrix], Optional[Error]]:
        """
        Get DH matrix for specified variable
        """
