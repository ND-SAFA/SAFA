import os
from enum import Enum

from constants import PROJ_PATH


class Domain(Enum):
    BASE = "base"
    AUTOMOTIVE = "automotive"
    SAFETY = "safety"
    ROBOTICS = "robotics"
    AEROSPACE = "aerospace"
    AG_TECH = "ag_tech"
    ENTERPRISE = "enterprise"
    DRONES = "drones"
    QUANTUM = "quantum"
    CHEMICAL = "chemical"
    ENERGY = "energy"


def get_path(domain_name: str):
    dir_ = os.path.dirname(os.path.relpath(__file__, PROJ_PATH))
    return os.path.join(dir_, domain_name)
