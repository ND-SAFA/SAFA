import os

from data.creators.parsers.definitions.structure_keys import StructureKeys
from data.formats.safa_format import SafaFormat
from util.file_util import FileUtil
from util.json_util import JSONUtil


class DatasetParser:

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.dataset_name = os.path.split(project_path)[-1]
        self.dataset_definition = FileUtil.read_json_file(self.dataset_definition_path)
        self.conversions = self.dataset_definition[StructureKeys.CONVERSIONS]

    def get_artifacts(self):
        JSONUtil.require_properties(self.dataset_definition, [SafaFormat.ARTIFACTS])
        return self.dataset_definition[SafaFormat.ARTIFACTS].items()

    def get_traces(self):
        JSONUtil.require_properties(self.dataset_definition, [SafaFormat.TRACES])
        return self.dataset_definition[SafaFormat.TRACES].items()
