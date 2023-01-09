from typing import Dict, List, Optional, Tuple

import pandas as pd

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.creators.readers.entity.entity_reader import EntityReader
from data.datasets.keys.safa_format import SafaKeys
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.json_util import JSONUtil
from util.uncased_dict import UncasedDict


class TraceEntityReader(EntityReader):
    """
    Responsible for reading trace links in a project.
    """

    ALLOW_MISSING_SOURCE = False
    ALLOW_MISSING_TARGET = False

    def __init__(self, base_path: str, trace_definition: Dict, type2artifacts: Dict[str, ArtifactReader], **kwargs):
        """
        Constructs trace entity reader for project at path and using definition.
        :param base_path: The path to the project.
        :param trace_definition: The definition instructing how to read traces.
        :param type2artifacts: The artifacts constructed for this project.
        :param kwargs: Additional parameters to construct entity reader with.
        """
        JSONUtil.require_properties(trace_definition, [SafaKeys.SOURCE_ID, SafaKeys.TARGET_ID])
        super().__init__(base_path, trace_definition, **kwargs)
        self.type2artifacts: Dict[str, ArtifactReader] = UncasedDict(type2artifacts)
        self.target_type = self.definition[SafaKeys.TARGET_ID]
        self.source_artifacts: List[Artifact] = self.type2artifacts[
            self.definition[SafaKeys.SOURCE_ID]].get_entities()
        self.target_artifacts: List[Artifact] = self.type2artifacts[
            self.definition[SafaKeys.TARGET_ID]].get_entities()

    def create(self, traces_df: pd.DataFrame) -> Dict[int, TraceLink]:
        """
        Creates trace links between source and target artifacts checking dataframe if link is positive or not.
        :param traces_df: DataFrame containing list of positive links.
        :return: Mapping between trace link id and the trace link.
        """
        trace_links: Dict[int, TraceLink] = {}
        n_positive = 0
        for source_artifact in self.source_artifacts:
            for target_artifact in self.target_artifacts:
                trace_link = self.create_trace_link(source_artifact, target_artifact, traces_df)
                trace_links[trace_link.id] = trace_link
                n_positive += 1 if trace_link.is_true_link else 0
        is_ok, msg = self.assert_missing_trace_links(traces_df)
        assert is_ok, msg
        return trace_links

    @staticmethod
    def create_trace_link(source_artifact: Artifact, target_artifact: Artifact, traces_df: pd.DataFrame) -> TraceLink:
        """
        Creates a trace link between artifacts checking matrix if link is positive or not.
        :param source_artifact: The source artifact to reference in trace link.
        :param target_artifact: The target artifact to reference in trace link.
        :param traces_df: DataFrame containing positive links in dataset.
        :return: TraceLink created.
        """
        source_id = source_artifact.id
        target_id = target_artifact.id
        trace_query = traces_df[(traces_df[SafaKeys.SOURCE_ID] == source_id) &
                                (traces_df[SafaKeys.TARGET_ID] == target_id)]
        is_positive = len(trace_query) >= 1
        return TraceLink(source_artifact, target_artifact, is_true_link=is_positive)

    def assert_missing_trace_links(self, traces_df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """
        Asserts that each trace link in DataFrame is created in dictionary. Otherwise, returns error if rule is turned on.
        :param traces_df: DataFrame containing positive links in project.
        :return: Tuple containing if trace links are okay as first element and error message as second element is not okay.
        """
        source_ids = [a.id for a in self.source_artifacts]
        target_ids = [a.id for a in self.target_artifacts]
        for _, row in traces_df.iterrows():
            source = row[SafaKeys.SOURCE_ID]
            target = row[SafaKeys.TARGET_ID]
            if source not in source_ids and not self.ALLOW_MISSING_SOURCE:
                return False, f"Undefined source in link: {source}"
            if target not in target_ids and not self.ALLOW_MISSING_TARGET:
                print("Undefined target in link:", target)
                return False, f"Undefined target in link: {target}"

        return True, None
