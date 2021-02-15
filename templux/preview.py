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

from typing import Any, Tuple
import pygame
from .camera import camera_ortho
pygame.init()


def preview_ortho(engine, args: Tuple[Any]):
    """
    Opens a preview window.
    :param engine: Function to do the rendering.
    :param args: List of arguments to pass to the engine, excluding the first (camera).
    """
    pygame.display.set_caption("Templux Preview")
    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    clock = pygame.time.Clock()
    width, height = 1280, 720
    last_width, last_height = 1280, 720
    resized = False

    cam_pos = [0, 0]
    cam_size = 5

    while True:
        clock.tick(60)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.VIDEORESIZE:
                last_width, last_height = width, height
                width, height = event.w, event.h
                resized = True

            elif event.type == pygame.ACTIVEEVENT and resized and width != last_width and height != last_height:
                surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                resized = False

        surface.fill((0, 0, 0))
        image = engine(camera_ortho((width, height), cam_pos, cam_size), *args)
        surface.blit(image, (0, 0))
