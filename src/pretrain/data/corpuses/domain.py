import os
from enum import Enum

from pretrain.config.paths import CORPUS_DIR


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
    return os.path.join(CORPUS_DIR, domain.value)
