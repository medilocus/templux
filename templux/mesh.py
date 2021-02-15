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
import struct


class Face:
    def __init__(self, verts) -> None:
        self.verts = verts

    def __repr__(self):
        return f"<Face {len(self.verts)} verts>"

    def __iter__(self):
        for v in self.verts:
            yield v


class Mesh:
    """Mesh class which stores faces and modifiers."""

    def __init__(self, faces: Tuple[Face]):
        self.faces = faces

    def __repr__(self):
        return f"<Mesh {len(self.faces)} faces>"

    @classmethod
    def from_stl_ascii(cls, path: str):
        with open(path, "r") as file:
            data = file.read()
            lines = data.strip().split("\n")
        if not lines[0].startswith("solid"):
            raise ValueError("First line does not start with \"solid\". Bad stl file.")

        faces = []
        curr_verts = []
        for line in lines:
            if line.startswith("vertex"):
                verts = list(map(float, line.replace("vertex", "").strip().split()))
                curr_verts.append(verts)
            if line.startswith("endloop"):
                faces.append(Face(curr_verts))
                curr_verts = []

        return cls(faces)

    @classmethod
    def from_stl_bin(cls, path: str):
        faces = []

        with open(path, "rb") as file:
            header = file.read(80)
            num_tris = file.read(4)
            num_tris = num_tris[0] + 2**8*num_tris[1] + 2**16*num_tris[2] + 2**24*num_tris[3]

            for i in range(num_tris):
                file.read(12)

                verts = []
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])

                faces.append(Face(verts))
                file.read(2)

        return cls(faces)
