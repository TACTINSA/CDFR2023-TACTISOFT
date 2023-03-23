import math
import time
from ctypes import *
from math import atan2, pi

import pygame as pygame

from tactisoft.movements import MecanumMovement
from tactisoft.pixy2.pixy import *
from tactisoft.pixy2 import pixy


class Vector(Structure):
    _fields_ = [
        ("m_x0", c_uint),
        ("m_y0", c_uint),
        ("m_x1", c_uint),
        ("m_y1", c_uint),
        ("m_index", c_uint),
        ("m_flags", c_uint)]


class IntersectionLine(Structure):
    _fields_ = [
        ("m_index", c_uint),
        ("m_reserved", c_uint),
        ("m_angle", c_uint)]


vectors = VectorArray(5)


def init_pxiy():
    pixy.init()
    pixy.change_prog("line")


def follow_line(movement: MecanumMovement, rotation_side_left: bool):
    pygame.init()
    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((78, 51))
    background = pygame.Surface((78, 51))
    background.fill(pygame.Color('#000000'))

    frame = 0
    has_turned = False
    correction_counter = 0
    while 1:
        window_surface.blit(background, (0, 0))
        line_get_main_features()
        v_count = line_get_vectors(5, vectors)
        if v_count > 0:
            print('frame %3d:' % frame)
            frame = frame + 1
            for index in range(0, v_count):
                print('[VECTOR: INDEX=%d X0=%d Y0=%d X1=%d Y1=%d]' % (vectors[index].m_index, vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1))
                pygame.draw.line(window_surface, (255, 0, 0), (vectors[index].m_x0, vectors[index].m_y0), (vectors[index].m_x1, vectors[index].m_y1))
                pygame.display.flip()

            primary_vector = vectors[0]
            length = ((primary_vector.m_x1 - primary_vector.m_x0) ** 2 + (primary_vector.m_y1 - primary_vector.m_y0) ** 2) ** 0.5
            angle = atan2(primary_vector.m_y1 - primary_vector.m_y0, primary_vector.m_x1 - primary_vector.m_x0) * 180 / pi + 90
            decallage = primary_vector.m_x0 - 39
            direction = pi / 2
            print("Length: " + str(length), "Angle: " + str(angle), "Decallage: " + str(decallage))
            if abs(angle) < 5:
                angle = 0

            if decallage > 5:
                angle += 10
            elif decallage < -5:
                angle -= 10
            print("Speed: " + str(90 * length / 40))
            movement.move(direction=direction, speed=max(60, min(90 * length / 40, 120)), turn=angle / 90)
        else:
            if not has_turned:
                movement.move(direction=pi / 2, speed=90)
                time.sleep(1.5)
                if rotation_side_left:
                    movement.turn_left(45)
                else:
                    movement.turn_right(45)
                has_turned = True
                time.sleep(2.5)
            else:
                movement.stop()
                time.sleep(0.5)
                movement.left(90)
                time.sleep(7)
                movement.backward(90)
                time.sleep(13)
                movement.right(90)
                time.sleep(3)
                has_turned = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        pygame.display.update()
