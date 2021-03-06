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

from typing import Dict, Tuple
from math import sin, cos, radians, sqrt
import numpy as np
import pygame
from ..mesh import Mesh, Face
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


def dist_to_cam(cam, face):
    cam_dist = 1000
    cam_rot_y, cam_rot_x = map(radians, cam["pos"])
    cam_z = cam_dist * cos(cam_rot_y)
    cam_x = cam_dist * sin(cam_rot_x) * sin(cam_rot_y)
    cam_y = cam_dist * cos(cam_rot_x) * sin(cam_rot_y) * -1

    # dist = 0
    # for x, y, z in face:
    #     dist += sqrt((cam_x-x)**2 + (cam_y-y)**2 + (cam_z-z)**2)
    # dist /= 3

    #dist = max([sqrt((cam_x-x)**2 + (cam_y-y)**2 + (cam_z-z)**2) for x, y, z in face])

    avg_point = [0, 0, 0]
    for x, y, z in face:
        avg_point[0] += x
        avg_point[1] += y
        avg_point[2] += z
    x, y, z = [x/3 for x in avg_point]
    dist = sqrt((cam_x-x)**2 + (cam_y-y)**2 + (cam_z-z)**2)

    return dist


def avg_vert(face):
    avg_point = [0, 0, 0]
    for x, y, z in face:
        avg_point[0] += x
        avg_point[1] += y
        avg_point[2] += z
    x, y, z = [x/3 for x in avg_point]

    return (x, y, z)


def sort_face_priority(cam, faces):
    sorted_faces = []
    cam_dist = 1000
    cam_rot_y, cam_rot_x = map(radians, cam["pos"])
    cam_z = cam_dist * cos(cam_rot_y)
    cam_x = cam_dist * sin(cam_rot_x) * sin(cam_rot_y)
    cam_y = cam_dist * cos(cam_rot_x) * sin(cam_rot_y)

    for face in faces:
        x, y, z = avg_vert(face)
        i = None
        for i in range(len(sorted_faces)):
            cx, cy, cz = avg_vert(sorted_faces[i])
            if cz > z and cam_z >= 0:
                break
            if cz < z and cam_z <= 0:
                break
            if cx > x and cam_x >= 0:
                break
            if cx < x and cam_x <= 0:
                break
            if cy > y and cam_y >= 0:
                break
            if cy < y and cam_y <= 0:
                break

        if i is None:
            sorted_faces.append(face)
        else:
            sorted_faces.insert(i, face)

    return sorted_faces


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
    #faces.sort(key=lambda face: dist_to_cam(cam, face), reverse=True)
    faces = sort_face_priority(cam, faces)

    for face in faces:
        vert_locs = [project(cam, vert) for vert in face]
        vert_locs = [normalize(cam, vert) for vert in vert_locs]
        mtcp_pos = matcap_pos(face.normal(), matcap.get_size())
        color = matcap.get_at(mtcp_pos)
        pygame.draw.polygon(surface, color, vert_locs)

    return surface
