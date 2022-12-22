from typing import Dict

from data.creators.parsers.artifact_parser import ArtifactParser
from data.creators.parsers.entity_parser import EntityParser
from data.formats.safa_format import SafaFormat
from data.tree.trace_link import TraceLink
from util.json_util import JSONUtil
from util.uncased_dict import UncasedDict


class TraceDefinition(EntityParser):
    def __init__(self, project_path: str, trace_definition: Dict,
                 type2artifacts: Dict[str, ArtifactParser], **kwargs):
        super().__init__(project_path, trace_definition, **kwargs)
        JSONUtil.require_properties(trace_definition, [SafaFormat.SOURCE_ID, SafaFormat.TARGET_ID])
        self.type2artifacts = UncasedDict(type2artifacts)
        self.traces = self.create()

    def create(self) -> Dict[int, TraceLink]:
        source_type = self.definition[SafaFormat.SOURCE_ID]
        target_type = self.definition[SafaFormat.TARGET_ID]
        traces_df = self.get_entities()

        source_artifact_definitions: ArtifactParser = self.type2artifacts[source_type]
        target_artifact_definitions: ArtifactParser = self.type2artifacts[target_type]

        positive_link_ids = []
        negative_link_ids = []
        trace_links: Dict[int, TraceLink] = {}
        for source_artifact in source_artifact_definitions.artifacts:
            for target_artifact in target_artifact_definitions.artifacts:
                trace_link = self.create_trace_link(source_artifact, target_artifact, traces_df)
                link_id_container = positive_link_ids if trace_link.is_true_link else negative_link_ids
                link_id_container.append(trace_link.id)
                trace_links[trace_link.id] = trace_link
        return trace_links

    @staticmethod
    def create_trace_link(source_artifact, target_artifact, traces_df):
        source_id = source_artifact.id
        target_id = target_artifact.id
        trace_query = traces_df[(traces_df[SafaFormat.SOURCE_ID] == source_id) &
                                (traces_df[SafaFormat.TARGET_ID] == target_id)]
        is_positive = len(trace_query) >= 1
        trace_link = TraceLink(source_artifact, target_artifact, is_true_link=is_positive)
        return trace_link
