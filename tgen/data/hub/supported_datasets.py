from tgen.data.hub.hub_ids.cchit_hub_id import CCHITHubId
from tgen.data.hub.hub_ids.cm1_hub_id import CM1HubId
from tgen.data.hub.hub_ids.drone_hub_id import DroneHubId
from tgen.data.hub.hub_ids.git_hub_id import GitHubId

from tgen.data.hub.hub_ids.iceoryx_hub_id import IceoryxHubId
from tgen.data.hub.hub_ids.itrust_hub_id import ITrustHubId
from tgen.data.hub.hub_ids.jpl_hub_id import JplHubId
from tgen.data.hub.hub_ids.mip_hub_id import MipHubId
from tgen.data.hub.hub_ids.train_controller_hub_id import TrainControllerHubId
from tgen.util.supported_enum import SupportedEnum


class SupportedDatasets(SupportedEnum):
    DRONE = DroneHubId
    ITRUST = ITrustHubId
    CM1 = CM1HubId
    MIP = MipHubId
    CCHIT = CCHITHubId
    TRAINCONTROLLER = TrainControllerHubId
    ICEORYX = IceoryxHubId
    GIT = GitHubId
    JPL = JplHubId
