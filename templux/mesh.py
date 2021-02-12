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

from typing import Tuple


class Face:
    pass


class Mesh:
    """Mesh class which stores faces and modifiers."""
    def __init__(self, faces: Tuple[Face]):
        self.faces = faces

    @classmethod
    def from_stl_ascii(cls, path: str):
        solid_started = False
        with open(path, "r") as file:
            line = file.readline()

            if not solid_started and not line.startswith("solid"):
                raise ValueError("Bad ASCII file. Does not contain \"solid\" at the beginning.")
            if line.startswith("solid"):
                solid_started = True
