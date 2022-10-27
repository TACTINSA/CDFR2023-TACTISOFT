from dataclasses import dataclass
from enum import IntEnum
from textwrap import wrap
from typing import List


@dataclass(frozen=True)
class Motors4:
    front_right: str
    front_left: str
    back_right: str
    back_left: str


@dataclass(frozen=True)
class Motors3:
    mot1: str
    mot2: str
    mot3: str


class Direction(IntEnum):
    """Representation of the direction for MKS SERVO42C. 0 means forward and 1 means backward."""
    FORWARD = 0
    BACKWARD = 1


def compute_rotation(direction: Direction, speed: int):
    """Compute motor rotation (direction + speed [0 - 127]). Return 1 byte (8 bits) encoded in hex. The highest bit
    indicates the direction, and the 7 lowest bits indicate 128 speed gears. """
    assert 0 < speed < 127, f"speed must be a number in range [0 - 127]. Currently speed is {speed}"
    return f"{(direction << 7) | speed:02x}"


def compute_distance(distance: int):
    """Compute the distance (number of pulse [0 - 2^64]). Return 4 bytes encoded in hex."""
    assert 0 < distance < 2 ** 64, f"distance must be a number in range [0 - 2^64]. Currently distance is {distance}"
    return wrap(f"{distance:08x}", 2)  # wrap(..., 2) split the result by bytes


def compute_validation(command: List):
    """Compute and return the validation byte (low byte of the sum of all bytes)"""
    return f"{sum([int(x, 16) for x in command]) & 0xFF:02x}"


def move(motor_id: str, direction: Direction, speed: int, distance: int = None) -> str:
    """Compute the command to move a motor (with or without distance)"""
    command = [motor_id]
    if distance is not None and distance != 0:
        command.append("fd")
    else:
        command.append("f6")

    command.append(compute_rotation(direction, speed))

    if distance is not None and distance != 0:
        command.extend(compute_distance(distance))

    command.append(compute_validation(command))
    return " ".join(command)


def stop(motor_id: str):
    """Compute the command to stop a motor"""
    command = [motor_id, "f7"]
    command.append(compute_validation(command))
    return " ".join(command)
