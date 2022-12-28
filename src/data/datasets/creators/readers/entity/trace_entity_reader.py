from typing import Dict, List, TypedDict

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.creators.readers.entity.entity_reader import EntityReader
from data.datasets.keys.safa_format import SafaKeys
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.json_util import JSONUtil
from util.uncased_dict import UncasedDict


class TraceData(TypedDict):
    source: str
    target: str


class TraceEntityReader(EntityReader):

    def __init__(self, base_path: str, trace_definition: Dict,
                 type2artifacts: Dict[str, ArtifactReader], **kwargs):
        JSONUtil.require_properties(trace_definition, [SafaKeys.SOURCE_ID, SafaKeys.TARGET_ID])
        super().__init__(base_path, trace_definition, **kwargs)
        self.type2artifacts: Dict[str, ArtifactReader] = UncasedDict(type2artifacts)
        self.target_type = self.definition[SafaKeys.TARGET_ID]
        self.source_artifacts: List[Artifact] = self.type2artifacts[
            self.definition[SafaKeys.SOURCE_ID]].get_entities()
        self.target_artifacts: List[Artifact] = self.type2artifacts[
            self.definition[SafaKeys.TARGET_ID]].get_entities()

    def create(self, traces_df) -> Dict[int, TraceLink]:
        positive_link_ids = []
        negative_link_ids = []
        trace_links: Dict[int, TraceLink] = {}
        for source_artifact in self.source_artifacts:
            for target_artifact in self.target_artifacts:
                trace_link = self.create_trace_link(source_artifact, target_artifact, traces_df)
                link_id_container = positive_link_ids if trace_link.is_true_link else negative_link_ids
                link_id_container.append(trace_link.id)
                trace_links[trace_link.id] = trace_link
        return trace_links

    @staticmethod
    def create_trace_link(source_artifact, target_artifact, traces_df):
        source_id = source_artifact.id
        target_id = target_artifact.id
        trace_query = traces_df[(traces_df[SafaKeys.SOURCE_ID] == source_id) &
                                (traces_df[SafaKeys.TARGET_ID] == target_id)]
        is_positive = len(trace_query) >= 1
        trace_link = TraceLink(source_artifact, target_artifact, is_true_link=is_positive)
        return trace_link
