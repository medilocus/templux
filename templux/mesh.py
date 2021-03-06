#
#  Templux
#  3D rendering engine for Python.
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
import numpy as np


class Face:
    verts: Tuple[Tuple[float]]

    def __init__(self, verts) -> None:
        self.verts = verts

    def __repr__(self):
        return f"<Face {len(self.verts)} verts>"

    def __iter__(self):
        for v in self.verts:
            yield v

    def __len__(self):
        return len(self.verts)

    def normal(self):
        p1, p2, p3 = map(np.array, self.verts)
        a = p2 - p1
        b = p3 - p1

        nx = a[1]*b[2] - a[2]*b[1]
        ny = a[2]*b[0] - a[0]*b[2]
        nz = a[0]*b[1] - a[1]*b[0]

        return (nx, ny, nz)


class Mesh:
    """Mesh class which stores faces."""

    faces: Tuple[Face]

    def __init__(self, faces: Tuple[Face]):
        self.faces = faces

    def __repr__(self):
        return f"<Mesh {len(self.faces)} faces>"

    @classmethod
    def from_stl_ascii(cls, path: str):
        with open(path, "r") as file:
            data = file.read()
            lines = [l.strip() for l in data.strip().split("\n")]
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
            num_tris = struct.unpack("<I", file.read(4))[0]

            for i in range(num_tris):
                file.read(12)

                verts = []
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])
                verts.append([struct.unpack("f", file.read(4))[0] for _ in range(3)])

                faces.append(Face(verts))
                file.read(2)

        return cls(faces)

    def save_stl_ascii(self, path: str, name: str = ""):
        with open(path, "w") as file:
            file.write(f"solid {name}\n")
            for face in self.faces:
                normal = face.normal()
                file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                file.write("    outer loop\n")
                for x, y, z in face:
                    file.write(f"        vertex {x} {y} {z}\n")
                file.write("    endloop\n")
                file.write("endfacet\n")

    def save_stl_bin(self, path: str, header: bytes = b""):
        with open(path, "wb") as file:
            header = header[:80]
            header += b" " * (80-len(header))
            num_tris = struct.pack("<I", len(self.faces))

            file.write(header)
            file.write(num_tris)
            for face in self.faces:
                normal = b"".join([struct.pack("f", nrm) for nrm in face.normal()])
                file.write(normal)
                for x, y, z in face:
                    data = struct.pack("f", x) + struct.pack("f", y) + struct.pack("f", z)
                    file.write(data)
                file.write(b"  ")

    def triangulate(self):
        faces = []

        for face in self.faces:
            if len(face) == 3:
                faces.append(face)
            else:
                for i in range(1, len(face)-1):
                    curr_face = Face(face[0], face[i], face[i+1])
                    faces.append(curr_face)

        return Mesh(faces)
