import os
from enum import Enum

from config.constants import PROJ_PATH


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


def get_path(domain: Domain):
    """
    Gets the path to the domain corpus
    :param domain: the Domain
    :return: the path to the domain corpus
    """
    dir_ = os.path.dirname(os.path.relpath(__file__, PROJ_PATH))
    return os.path.join(dir_, domain.value)
