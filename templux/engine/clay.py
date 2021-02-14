#
#  Graphic Videos
#  An API for creating graphic videos in Python.
#  Copyright Medilocus 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from typing import Dict, Tuple
from math import sin, cos, radians
from ..mesh import Mesh


def normalize(cam, loc):
    res = cam["res"]
    x = loc[0]/cam["size"]*res[0] + res[0]/2
    y = loc[1]/cam["size"]*res[0] + res[1]/2
    return (x, y)


def project(cam, loc):
    x, y, z = loc
    view_y, view_x = map(lambda x: radians(x), cam["pos"])

    len_x = 0
    len_y = 0

    len_x += cos(view_x) * x
    len_x += sin(view_x) * y

    len_y += sin(view_x) * cos(view_y) * x
    len_y -= cos(view_x) * cos(view_y) * y
    len_y -= sin(view_y) * z

    return (len_x, len_y)


def render_wire(cam: Dict, meshes: Tuple[Mesh]) -> Dict:
    pass
