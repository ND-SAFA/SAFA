import os
from typing import Dict, List, Set

from tgen.common.constants.tracing.code_tracer_constants import C_IMPLEMENTATION_EXTENSIONS, DEFAULT_CHILD_LAYER_ID, \
    DEFAULT_RENAME_CHILDREN, HEADER_EXTENSIONS, HEADER_FILE_EXPLANATION, PACKAGE_EXPLANATION, PACKAGE_TYPE
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
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

    def trace(self):
        self.add_code_traces()
        self.add_package_nodes()

    def add_code_traces(self, rename_children: bool = DEFAULT_RENAME_CHILDREN) -> None:
        """
        Adds trace links between code files.
        :return: None (modifies the trace dataset).
        """
        # TODO allow user to supply new name for child layer if renaming
        artifact_df = self.trace_dataset.artifact_df
        artifact_ids = list(artifact_df.index)

        header_files = FileUtil.filter_by_ext(artifact_ids, HEADER_EXTENSIONS)
        implementation_files = FileUtil.filter_by_ext(artifact_ids, C_IMPLEMENTATION_EXTENSIONS)
        header_links = CodeTracer.trace_by_base_names(header_files, implementation_files)

        if rename_children:
            self._rename_child_files(implementation_files, header_files)

        # TODO: Add conditions for other programming languages

        links = header_links
        self.trace_dataset.trace_df.add_links(links)

    def add_package_nodes(self, package_type: str = PACKAGE_TYPE) -> None:
        """
        Extracts packages and adds them as artifacts.
        :return: None (artifact data frame is modified)
        """
        artifact_ids = self.trace_dataset.artifact_df.index
        artifact_ids_set = set(artifact_ids)
        packages = CodeTracer.extract_packages(artifact_ids)
        original_artifact_types = self.trace_dataset.artifact_df[ArtifactKeys.LAYER_ID.value].unique()

        links = []
        trace_ids = set()
        for parent_node, children in packages.items():
            if parent_node not in artifact_ids_set:
                CodeTracer.add_package(self.trace_dataset, artifact_ids_set, parent_node, package_type)
            for child_node in children:
                if child_node not in artifact_ids_set:
                    CodeTracer.add_package(self.trace_dataset, artifact_ids_set, child_node, package_type)
                trace_id = TraceDataFrame.generate_link_id(source_id=child_node, target_id=parent_node)
                if trace_id not in trace_ids:
                    trace_entry = TracePredictionEntry(
                        source=child_node,
                        target=parent_node,
                        label=1,
                        explanation=PACKAGE_EXPLANATION
                    )
                    links.append(trace_entry)
                    trace_ids.add(trace_id)
                else:
                    logger.info(f"Found duplicate package relationship: {parent_node} -> {child_node}")
        self.trace_dataset.trace_df.add_links(links)
        self.trace_dataset.layer_df.add_layer(source_type=package_type, target_type=package_type)
        for original_artifact_type in original_artifact_types:
            self.trace_dataset.layer_df.add_layer(source_type=original_artifact_type, target_type=package_type)

    def _rename_child_files(self, parent_ids: List[str], child_ids: List[str],
                            child_layer_id: str = DEFAULT_CHILD_LAYER_ID):
        """
        Updates the children artifact to have a specified layer id if it matches any of the parent artifacts.
        :param parent_ids: The list of parent ids.
        :param child_ids: The list of children ids.
        :param child_layer_id: The layer id to rename the children to.
        :return: None (modifies artifact data frame).
        """
        parent_layer_ids = set([self.trace_dataset.artifact_df.get_artifact(p_id)[ArtifactKeys.LAYER_ID] for p_id in parent_ids])
        for c_id in child_ids:
            c_artifact = self.trace_dataset.artifact_df.get_artifact(c_id)
            if c_artifact[ArtifactKeys.LAYER_ID] in parent_layer_ids:
                self.trace_dataset.artifact_df.update_value(column2update=ArtifactKeys.LAYER_ID,
                                                            id2update=c_id,
                                                            new_value=child_layer_id)
        for p_layer_id in parent_layer_ids:
            self.trace_dataset.layer_df.add_layer(source_type=child_layer_id, target_type=p_layer_id)

    @staticmethod
    def add_package(trace_dataset: TraceDataset, artifact_ids_set: Set[str], package_name: str, package_type: str):
        trace_dataset.artifact_df.add_artifact(artifact_id=package_name,
                                               layer_id=package_type,
                                               content="",
                                               summary="")
        artifact_ids_set.add(package_name)

    @staticmethod
    def extract_packages(file_paths: List[str]) -> Dict[str, List[str]]:
        """
        Extracts the list of packages references in the list of file paths.
        :param file_paths: The file paths to source code.
        :return: List of unique packages.
        """
        packages = {}
        for file_path in file_paths:
            file_packages = FileUtil.split_into_parts(file_path)
            for i in range(0, len(file_packages) - 1):
                parent = os.path.join(*file_packages[:i + 1])
                child = os.path.join(*file_packages[:i + 2])
                if parent not in packages:
                    packages[parent] = set()
                if child not in packages[parent]:
                    packages[parent].add(child)

        packages = {p: list(c) for p, c in packages.items()}
        return packages

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
                                                      label=1,
                                                      explanation=HEADER_FILE_EXPLANATION)
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
