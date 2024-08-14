from typing import Dict, List

from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.trace_dataset import TraceDataset

from tgen.common.constants.code_tracer_constants import C_IMPLEMENTATION_EXTENSIONS, DEFAULT_CHILD_LAYER_ID, DEFAULT_RENAME_CHILDREN, \
    HEADER_EXTENSIONS, HEADER_FILE_EXPLANATION
from common_resources.tools.t_logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from common_resources.tools.util.file_util import FileUtil
from tgen.tracing.code.package_tracer import PackageTracer


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

    def trace(self, add_packages: bool = True):
        """
        Adds traces between code modules and optionally adds packages as artifacts.
        :param add_packages: Whether to add package nodes to trace dataset.
        :return: None (dataset is modified)
        """
        self.add_code_traces()
        if add_packages:
            self.add_package_nodes()

    def add_code_traces(self, rename_children: bool = DEFAULT_RENAME_CHILDREN) -> None:
        """
        Adds trace links between code files.
        :param rename_children: Whether to rename the children to contain the layer id names might conflict.
        :return: None (modifies the trace dataset).
        """
        # TODO allow user to supply new name for child layer if renaming
        artifact_df = self.trace_dataset.artifact_df
        artifact_ids = list(artifact_df.index)

        header_files = FileUtil.filter_by_ext(artifact_ids, HEADER_EXTENSIONS)
        implementation_files = FileUtil.filter_by_ext(artifact_ids, C_IMPLEMENTATION_EXTENSIONS)
        header_links = CodeTracer.trace_by_base_names(header_files, implementation_files)

        logger.info(f"{len(header_files)} header files found.")
        logger.info(f"{len(implementation_files)} implementation files found.")
        logger.info(f"{len(header_links)} links found between header and implementation files.")

        if rename_children:
            self._rename_child_files(implementation_files, header_files)

        # TODO: Add conditions for other programming languages

        links = header_links
        self.trace_dataset.trace_df.add_links(links)

    def add_package_nodes(self) -> None:
        """
        Extracts packages and adds them as artifacts.
        :return: None (artifact data frame is modified)
        """
        PackageTracer.add_package_nodes(self.trace_dataset)

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
    def trace_by_base_names(child_paths: List[str], parent_paths: List[str]) -> List[Trace]:
        """
        Traces the child files to the parent files based on their file base names.
        :param child_paths: List of children file paths.
        :param parent_paths: List of parent file paths.
        :return: List of trace links.
        """
        child_map = CodeTracer.create_base_name_map(child_paths)
        parent_map = CodeTracer.create_base_name_map(parent_paths)

        links: List[Trace] = []
        for child_base, child_paths in child_map.items():
            if child_base in parent_map:
                for child_path in child_paths:
                    for parent_path in parent_map[child_base]:
                        t_link = Trace(source=child_path,
                                       target=parent_path,
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
