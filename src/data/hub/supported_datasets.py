from data.hub.hub_descriptors.cchit_descriptor import CCHITDescriptor
from data.hub.hub_descriptors.cm1_descriptor import CM1Descriptor
from data.hub.hub_descriptors.drone_nl_descriptor import DroneNLDescriptor
from data.hub.hub_descriptors.drone_pl_descriptor import DronePLDescriptor
from data.hub.hub_descriptors.itrust_descriptor import ITrustDescriptor
from data.hub.hub_descriptors.mip_descriptor import MipDescriptor
from data.hub.hub_descriptors.train_controller_descriptor import TrainControllerDescriptor
from util.supported_enum import SupportedEnum


class SupportedDatasets(SupportedEnum):
    CCHIT = CCHITDescriptor
    CM1 = CM1Descriptor
    TRAINCONTROLLER = TrainControllerDescriptor
    DRONE_PL = DronePLDescriptor
    DRONE_NL = DroneNLDescriptor
    ITRUST = ITrustDescriptor
    MIP = MipDescriptor
