from typing import Dict, List

from tgen.common.constants.tracing.code_tracer_constants import C_IMPLEMENTATION_EXTENSIONS, HEADER_EXTENSION
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

        header_links = self.trace_header_files(artifact_ids)

        # TODO: Add conditions for other programming languages
        links: List[TracePredictionEntry] = header_links
        return links

    @staticmethod
    def trace_header_files(file_paths: List[str]) -> List[TracePredictionEntry]:
        """
        Traces C-based implementation files to their header files.
        :param file_paths: The file paths to trace.
        :return: List of trace links.
        """
        h_files = FileUtil.filter_by_ext(file_paths, HEADER_EXTENSION)
        implementation_files = FileUtil.filter_by_ext(file_paths, C_IMPLEMENTATION_EXTENSIONS)
        links = CodeTracer.trace_by_base_names(h_files, implementation_files)
        return links

    @staticmethod
    def trace_by_base_names(child_paths: List[str], parent_paths: List[str]) -> List[TracePredictionEntry]:
        """
        Traces the child files to the parent files based on their file base names.
        :param child_paths: List of children file paths.
        :param parent_paths: List of parent file paths.
        :return: List of trace links.
        """
        child_map = CodeTracer.create_base_name_map(child_paths)
        parent_map = CodeTracer.create_base_name_map(parent_paths)

        links: List[TracePredictionEntry] = []
        for child_base, child_paths in child_map.items():
            if child_base in parent_map:
                for child_path in child_paths:
                    for parent_path in parent_map[child_base]:
                        t_link = TracePredictionEntry(source=child_path,
                                                      target=parent_path,
                                                      score=1,
                                                      explanation="Files have the same name.")
                        links.append(t_link)
        return links

    @staticmethod
    def create_base_name_map(file_paths: List[str]) -> Dict[str, List[str]]:
        """
        Maps base name to list of file paths with that base name.
        :param file_paths: The file paths to map.
        :return: Mapping of base names to file paths.
        """
        base_name_map = {}
        for f_path in file_paths:
            f_base_name = FileUtil.get_file_base_name(f_path)
            if f_base_name not in base_name_map:
                base_name_map[f_base_name] = []
            base_name_map[f_base_name].append(f_path)
        return base_name_map
