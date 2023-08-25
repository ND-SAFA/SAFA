from typing import List

from tgen.common.util.file_util import FileUtil
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.tdatasets.trace_dataset import TraceDataset


class CodeTracer:
    """
    Traces between code files.
    C / C++ : Connects header to implementation files.
    """

    def __init__(self, trace_dataset: TraceDataset):
        """
        Constructs code tracer with trace dataset artifacts and trace links.
        :param trace_dataset: The dataset containing code to trace.
        """
        self.trace_dataset = trace_dataset

    def trace(self) -> List[TracePredictionEntry]:
        """
        Traces the code files in the trace dataset
        :return:
        """
        artifact_df = self.trace_dataset.artifact_df
        artifact_ids = list(artifact_df.index)

        header_files = FileUtil.filter_by_ext(artifact_ids, ".h")
        cc_files = FileUtil.filter_by_ext(artifact_ids, ".cc")
        cpp_files = FileUtil.filter_by_ext(artifact_ids, ".cpp")

        h2cc = self.trace_by_base_names(header_files, cc_files)
        h2cpp = self.trace_by_base_names(header_files, cpp_files)

        # TODO: Add conditions for other programming languages

        links: List[TracePredictionEntry] = h2cc + h2cpp
        return links

    @staticmethod
    def trace_by_base_names(child_paths: List[str], parent_paths: List[str]) -> List[TracePredictionEntry]:
        """
        Traces the child files to the parent files based on their file base names.
        :param child_paths: List of children file paths.
        :param parent_paths: List of parent file paths.
        :return: List of trace links.
        """
        source_map = {FileUtil.get_file_base_name(p): p for p in child_paths}
        target_map = {FileUtil.get_file_base_name(p): p for p in parent_paths}

        links: List[TracePredictionEntry] = []
        for s_base, s_path in source_map.items():
            if s_base in target_map:
                t_path = target_map[s_base]
                t_link = TracePredictionEntry(source=s_path, target=t_path, score=1, explanation="Files have the same name.")
                links.append(t_link)
        return links
