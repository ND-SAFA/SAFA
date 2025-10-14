from typing import Any, Dict, List, Set, Type, Union

import numpy as np

from gen_common.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from gen_common.data.keys.structure_keys import StructuredKeys, TraceKeys, TraceRelationshipType
from gen_common.data.objects.trace import Trace
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.dict_util import DictUtil
from gen_common.util.enum_util import EnumDict


class TraceDataFrame(AbstractProjectDataFrame):
    """
    Contains the trace links found in a project
    """
    OPTIONAL_COLUMNS = [StructuredKeys.Trace.LABEL.value,
                        StructuredKeys.Trace.SCORE.value,
                        StructuredKeys.Trace.EXPLANATION.value,
                        StructuredKeys.Trace.RELATIONSHIP_TYPE.value]
    DEFAULT_FOR_OPTIONAL_COLS = EnumDict({StructuredKeys.Trace.RELATIONSHIP_TYPE: TraceRelationshipType.TRACEABILITY,
                                          StructuredKeys.Trace.LABEL.value: np.NAN,
                                          StructuredKeys.Trace.SCORE.value: np.NAN,
                                          StructuredKeys.Trace.EXPLANATION.value: None})

    def __init__(self, *args, **kwargs):
        """
        Creates constructor with guaranteed columns for trace dataframe.
        :param args: The positional arguments to constructor trace dataframe with.
        :param kwargs: The keyword arguments to construct trace dataframe with.
        """
        DictUtil.update_kwarg_values(kwargs, replace_existing=False, columns=StructuredKeys.Trace.get_cols())
        super().__init__(*args, **kwargs)

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return TraceKeys.LINK_ID.value

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return TraceKeys

    def process_data(self) -> None:
        """
        Sets the index of the dataframe and performs any other processing steps
        :return: None
        """
        self.add_link_ids()
        super().process_data()

    def add_link_ids(self) -> None:
        """
        Adds the link ids column to the df
        :return: None
        """
        if self.columns.empty:
            return
        if TraceKeys.LINK_ID.value not in self.columns and self.index.name != self.index_name():
            link_ids = []
            for index, row in self.itertuples():
                link_ids.append(TraceDataFrame.generate_link_id(row[TraceKeys.SOURCE], row[TraceKeys.TARGET]))
            self[TraceKeys.LINK_ID] = link_ids

    def add_links(self, links: List[Trace]) -> None:
        """
        Adds links to data frame.
        :param links: The trace predictions to add.
        :return: None (data frame is modified).
        """
        for link in links:
            self.add_link(source=link["source"], target=link["target"], label=link["label"], score=link.get("score", None),
                          explanation=link.get("explanation", None))

    def add_link(self, source: str, target: str,
                 label: int = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.LABEL],
                 score: float = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.SCORE],
                 explanation: str = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.EXPLANATION],
                 relationship_type: Union[TraceRelationshipType, str] = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.RELATIONSHIP_TYPE]) \
            -> EnumDict:
        """
        Adds link to dataframe
        :param source: The id of the source
        :param target: The id of the target
        :param label: The label of the link (1 if True link, 0 otherwise)
        :param score: The score of the generated links.
        :param explanation: The explanation for generated trace link.
        :param relationship_type: The type of relationship between the artifacts.
        :return: The newly added link
        """
        link_id = TraceDataFrame.generate_link_id(source, target)
        return self.add_row(
            self.link_as_dict(source_id=source, target_id=target, link_id=link_id, label=label, score=score, explanation=explanation,
                              relationship_type=relationship_type))

    def get_links(self, true_only: bool = False, true_link_threshold: float = 0) -> List[EnumDict]:
        """
        Returns the links in the data frame.
        :param true_only: If True, only returns links with positive id.
        :param true_link_threshold: If selecting positive links only, considers scored links as true if above threshold.
        (Set to None to only consider links with labels)
        :return: Traces in data frame.
        """
        true_only = true_only or bool(true_link_threshold)
        links = [link for link_id, link in self.itertuples() if not true_only or
                 self.is_true_link(link, true_link_threshold=true_link_threshold)]
        return links

    @staticmethod
    def is_true_link(link: EnumDict, true_link_threshold: float = 0) -> bool:
        """
        Determines whether the link is a true (positive) link.
        :param link: The link to determine if it is true.
        :param true_link_threshold: If selecting positive links only, considers scored links as true if above threshold.
        (Set to None to only consider links with labels)
        """
        use_scores = true_link_threshold is not None
        if link[TraceKeys.LABEL] == 0:
            return False
        return link[TraceKeys.LABEL] == 1 or (use_scores and link[TraceKeys.SCORE] >= true_link_threshold)

    def get_link(self, link_id: int = None, source_id: Any = None, target_id: Any = None) -> EnumDict:
        """
        Gets the row of the dataframe with the associated link_id or source and target id
        :param link_id: The id of the link to get. May provide source and target id instead
        :param source_id: The id of the source, only required if link_id is not specified
        :param target_id: The id of the target, only required if link_id is not specified
        :return: The link if one is found with the specified params, else None
        """
        if link_id is None:
            assert source_id is not None and target_id is not None, "Requires source_id and target_id if no link_id is provided."
            link_id = TraceDataFrame.generate_link_id(source_id, target_id)
        return self.get_row(link_id)

    @staticmethod
    def link_as_dict(source_id: str, target_id: str, link_id: int = None, label: int = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.LABEL],
                     score: float = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.SCORE],
                     explanation: str = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.EXPLANATION],
                     relationship_type: str = DEFAULT_FOR_OPTIONAL_COLS[TraceKeys.RELATIONSHIP_TYPE]) \
            -> Dict[TraceKeys, Any]:
        """
        Creates a dictionary mapping column names to the corresponding link information
        :param source_id: The id of the source artifact
        :param target_id: The id of the target artifact
        :param label: The label of the link (1 if True link, 0 otherwise)
        :param link_id: The id of the link
        :param score: The score of the generated link.
        :param explanation: Explanation for generated trace link.
        :param relationship_type: The type of relationship between the artifacts.
        :return: A dictionary mapping column names to the corresponding link information
        """
        relationship_type = relationship_type
        dict_ = {TraceKeys.LINK_ID: link_id} if link_id else {}
        dict_.update({TraceKeys.SOURCE: source_id, TraceKeys.TARGET: target_id,
                      TraceKeys.LABEL: label, TraceKeys.SCORE: score, TraceKeys.EXPLANATION: explanation,
                      TraceKeys.RELATIONSHIP_TYPE: relationship_type})
        return EnumDict(dict_)

    @staticmethod
    def generate_link_id(source_id: Any, target_id: Any) -> int:
        """
        Generates a unique id for a source, target link
        :param source_id: id of source artifact
        :param target_id: id of target artifact
        :return: the link id
        """
        return hash(str(hash(source_id)) + "-" + str(hash(target_id)))

    def get_label_count(self, label: int = 1) -> int:
        """
        :param label: The label whose count is returned.
        :return: Returns the number of true positives in data frame.
        """
        label_counts = self[TraceKeys.LABEL].value_counts()
        n_label = label_counts.get(label, 0)
        return n_label

    def get_links_with_label(self, label: int):
        """
        :param label: Either 0 or 1.
        :return: Returns links with given label.
        """
        return [t for t_id, t in self.itertuples() if t[TraceKeys.LABEL] == label]

    def to_map(self) -> Dict:
        """
        Creates a map of ID to trace link.
        :return: Mapping of trace links.
        """
        t_map = {}
        for i, row in self.itertuples():
            t_map[i] = row
        return t_map

    def get_orphans(self, artifact_role: TraceKeys = TraceKeys.child_label(), true_link_threshold: float = None) -> Set[Any]:
        """
        Returns all orphans that are of the given role (parent or child)
        :param artifact_role: The role of the artifact as either a parent (target) or child (source)
        :param true_link_threshold: If selecting positive links only, considers scored links as true if above threshold.
        :return: Ids of all orphans that are of the given role (parent or child)
        """
        all_artifact_ids = self.get_artifact_ids(artifact_role=artifact_role, linked_only=False)
        orphans = self.find_orphans(self.get_links(true_only=True, true_link_threshold=true_link_threshold),
                                    all_artifact_ids, artifact_role)
        return orphans

    @staticmethod
    def find_orphans(true_traces: List[EnumDict], all_artifact_ids: Set[str],
                     artifact_role: TraceKeys = TraceKeys.child_label()) -> Set[Any]:
        """
        Returns all orphans in the given traces that are of the given role (parent or child)
        :param true_traces: The traces to look for orphans in.
        :param all_artifact_ids: A set of all artifact ids that could have traces.
        :param artifact_role: The role of the artifact as either a parent (target) or child (source)
        :return: Ids of all orphans that are of the given role (parent or child)
        """
        linked_artifacts = {trace[artifact_role] for trace in true_traces}
        orphans = all_artifact_ids.difference(linked_artifacts)
        return orphans

    def get_parent_ids(self, artifact_id: str) -> List[str]:
        """
        Returns the parent artifact ids of given artifact.
        :param artifact_id: Id of artifact to find parents for.
        :return: Parent ids of artifact.
        """
        query_df = self.filter_for_parents_or_children(artifact_id)
        parent_ids = list(query_df[TraceKeys.TARGET.value])
        return parent_ids

    def filter_for_parents_or_children(self, artifact_id: str,
                                       artifact_key: Union[str, TraceKeys] = TraceKeys.child_label()) -> "TraceDataFrame":
        """
        Filters dataframe to find all children or parents of the artifact.
        :param artifact_id: The id to look for.
        :param artifact_key: The key that the artifact will be under (child label means all parents are returned and vice versa).
        :return: Dataframe with traces of only the children or parents of the artifact.
        """
        artifact_key = artifact_key.value if isinstance(artifact_key, TraceKeys) else artifact_key
        query_df = self.filter_by_row(lambda row: row[artifact_key] == artifact_id and
                                                  (DataFrameUtil.get_optional_value_from_df(row, TraceKeys.SCORE.value,
                                                                                            default_value=0) > 0
                                                   or row[TraceKeys.LABEL.value] == 1))
        return query_df

    def get_artifact_ids(self, artifact_role: TraceKeys = None, linked_only: bool = False) -> Set[str]:
        """
        Returns the artifact ids in the trace df.
        :param artifact_role: Will just get the sources or targets if appropriate key is provided, else all.
        :param linked_only: If True, will only get artifacts that are linked.
        :return: The artifact ids in the trace df.
        """
        artifact_ids = set()
        for trace in self.get_links(true_only=linked_only):
            for key in [TraceKeys.SOURCE, TraceKeys.TARGET]:
                if artifact_role and key != artifact_role:
                    continue
                artifact_ids.add(trace[key])
        return artifact_ids

    def get_relationships(self, artifact_ids: str | List[str] | Set[str], artifact_key: str = None) -> List[EnumDict]:
        """
        Finds traces related to the artifact.
        If an artifact key is provided, will only look for traces with trace[artifact_key] == artifact_id.
        :param artifact_ids: The id to look for.
        :param artifact_key: The key that the artifact will be under (child label means all parents are returned and vice versa).
        :return: List of all traces related to the artifact.
        """
        if isinstance(artifact_ids, str):
            artifact_ids = [artifact_ids]
        all_relationships = []
        for a_id in artifact_ids:
            for key in [TraceKeys.child_label(), TraceKeys.parent_label()]:
                if artifact_key == key or not artifact_key:
                    relations = self.filter_for_parents_or_children(a_id, key).get_links()
                    all_relationships.extend(relations)
        return all_relationships
