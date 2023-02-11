from data.hub.cchit_reader import CCHITReader
from util.supported_enum import SupportedEnum


class SupportedDatasets(SupportedEnum):
    CCHIT = CCHITReader
