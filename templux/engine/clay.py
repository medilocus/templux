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
from math import atan, sin, cos, radians, sqrt
import numpy as np
import pygame
from ..mesh import Mesh
pygame.init()


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

    len_y -= sin(view_x) * cos(view_y) * x
    len_y += cos(view_x) * cos(view_y) * y
    len_y += sin(view_y) * z

    return (len_x, len_y)


def normal(face):
    p1, p2, p3 = map(np.array, face)
    a = p2 - p1
    b = p3 - p1

    nx = a[1]*b[2] - a[2]*b[1]
    ny = a[2]*b[0] - a[0]*b[2]
    nz = a[0]*b[1] - a[1]*b[0]

    return (nx, ny, nz)


def matcap_pos(normal, size):
    size_x, size_y = size
    mag = sqrt(sum([x**2 for x in normal]))
    px, py, pz = np.array(normal) / mag

    x_loc = size_x * (px+1) / 2
    y_loc = size_y * (1-pz) / 2

    if x_loc >= size_x:
        x_loc = size_x - 1
    if y_loc >= size_y:
        y_loc = size_y - 1

    return list(map(int, (x_loc, y_loc)))


def render_wire(cam: Dict, meshes: Tuple[Mesh], color: Tuple[int], thickness: int = 2):
    """
    Renders meshes as wireframe.
    :param cam: Dictionary containing camera data.
    :param meshes: List of meshes to render.
    :param color: Color of wireframe.
    :param thickness: Thickness of wireframe.
    """
    surface = pygame.Surface(cam["res"], pygame.SRCALPHA)

    for mesh in meshes:
        for face in mesh.faces:
            locs = [project(cam, v) for v in face]
            locs = [normalize(cam, l) for l in locs]
            pygame.draw.line(surface, color, locs[0], locs[1], thickness)
            pygame.draw.line(surface, color, locs[0], locs[2], thickness)
            pygame.draw.line(surface, color, locs[1], locs[2], thickness)

    return surface


def render_solid(cam: Dict, meshes: Tuple[Mesh], matcap: pygame.Surface) -> pygame.Surface:
    """
    Renders meshes with matcap.
    :param cam: Dictionary containing camera data.
    :param meshes: List of meshes to render.
    :param matcap: Matcap pygame surface.
    """
    surface = pygame.Surface(cam["res"], pygame.SRCALPHA)
    faces = []
    for mesh in meshes:
        faces.extend(mesh.faces)

    for face in faces:
        vert_locs = [project(cam, vert) for vert in face]
        vert_locs = [normalize(cam, vert) for vert in vert_locs]
        mtcp_pos = matcap_pos(normal(face), matcap.get_size())
        color = matcap.get_at(mtcp_pos)
        pygame.draw.polygon(surface, color, vert_locs)

    return surface
