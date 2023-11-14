from typing import Any, Dict, List, Type, Set

import numpy as np

from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import StructuredKeys, TraceKeys


class TraceDataFrame(AbstractProjectDataFrame):
    """
    Contains the trace links found in a project
    """
    OPTIONAL_COLUMNS = [StructuredKeys.Trace.LABEL.value,
                        StructuredKeys.Trace.SCORE.value,
                        StructuredKeys.Trace.EXPLANATION.value]

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

    def add_link(self, source: str, target: str, label: int = 0, score: float = np.NAN, explanation: str = None) -> EnumDict:
        """
        Adds link to dataframe
        :param source: The id of the source
        :param target: The id of the target
        :param label: The label of the link (1 if True link, 0 otherwise)
        :param score: The score of the generated links.
        :param explanation: The explanation for generated trace link.
        :return: The newly added link
        """
        link_id = TraceDataFrame.generate_link_id(source, target)
        return self.add_or_update_row(
            self.link_as_dict(source_id=source, target_id=target, label=label, link_id=link_id, score=score,
                              explanation=explanation))

    def get_links(self) -> List[EnumDict]:
        """
        Returns the links in the data frame.
        :return: Traces in data frame.
        """
        links = []
        for link_id in self.index:
            links.append(self.get_link(link_id))
        return links

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
    def link_as_dict(source_id: str, target_id: str, label: int = 0, link_id: int = None, score: float = np.NAN,
                     explanation: str = None) -> Dict[TraceKeys, Any]:
        """
        Creates a dictionary mapping column names to the corresponding link information
        :param source_id: The id of the source artifact
        :param target_id: The id of the target artifact
        :param label: The label of the link (1 if True link, 0 otherwise)
        :param link_id: The id of the link
        :param score: The score of the generated link.
        :param explanation: Explanation for generated trace link.
        :return: A dictionary mapping column names to the corresponding link information
        """
        dict_ = EnumDict({TraceKeys.LINK_ID: link_id} if link_id else {})
        dict_.update({TraceKeys.SOURCE: source_id, TraceKeys.TARGET: target_id, TraceKeys.LABEL: label, TraceKeys.SCORE: score,
                      TraceKeys.EXPLANATION: explanation})
        return dict_

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

    def get_orphans(self, artifact_role: TraceKeys = TraceKeys.child_label()) -> Set[Any]:
        """
        Returns all orphans that are of the given role (parent or child)
        :param artifact_role: The role of the artifact as either a parent (target) or child (source)
        :return: Ids of all orphans that are of the given role (parent or child)
        """
        linked_artifacts = {trace[artifact_role] for i, trace in self.itertuples()
                            if trace[TraceKeys.LABEL] == 1}
        orphans = {trace[artifact_role] for i, trace in self.itertuples()
                   if trace[artifact_role] not in linked_artifacts}
        return orphans
