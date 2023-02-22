from data.hub.hub_ids.cchit_hub_id import CCHITHubId
from data.hub.hub_ids.cm1_hub_id import CM1HubId
from data.hub.hub_ids.drone_hub_id import DroneNLHubId
from data.hub.hub_ids.drone_pl_hub_id import DronePLHubId
from data.hub.hub_ids.iceoryx_pl import ICEORYXPLHubId
from data.hub.hub_ids.itrust_hub_id import ITrustHubId
from data.hub.hub_ids.mip_hub_id import MipHubId
from data.hub.hub_ids.train_controller_hub_id import TrainControllerHubId
from util.supported_enum import SupportedEnum


class SupportedDatasets(SupportedEnum):
    CCHIT = CCHITHubId
    CM1 = CM1HubId
    TRAINCONTROLLER = TrainControllerHubId
    DRONE_PL = DronePLHubId
    DRONE_NL = DroneNLHubId
    ITRUST = ITrustHubId
    MIP = MipHubId
    ICEORYX_PL = ICEORYXPLHubId
