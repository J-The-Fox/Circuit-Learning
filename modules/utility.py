"""
This File Holds Functions And Methods That Don't Fit In With Any Other Module.
"""

from typing import Union, Tuple, Sequence
from pygame.math import Vector2
from pygame.color import Color

__all__ = ['Coordinate', 'RGBAOutput', 'ColorValue', 'Dimension', 'Range', 'strtobool']

# -----=====[Type Aliases]=====----- #
# Imported From pygame._common
Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
# Custom
Dimension = Tuple[int, int]
Range = Union[Tuple[float, float], Sequence[float]]


# -----=====[Functions]=====----- #

def strtobool (val: str):
    """
    Convert A String Representation Of Truth To True Or False.

    True Values Are: 'y', 'yes', 't', 'true', 'on', and '1';
    False Values Are: 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.  

    Note: Copied From Python 2's distutils.util Module.
    """

    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("Invalid Truth Value %r" % (val,))