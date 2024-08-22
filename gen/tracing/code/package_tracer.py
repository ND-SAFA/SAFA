import os
from typing import Dict, Iterable, List, Tuple

from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.file_util import FileUtil

from gen.constants.code_tracer_constants import DEFAULT_PACKAGE_ARTIFACT_TYPE, PACKAGE_EXPLANATION


class PackageTracer:
    """
    Creates package nodes from source code.
    - Add package artifacts
    - Add links from packages to code artifacts
    - (Optional) Migrates links between source code and other artifacts to the packages of the source codes
    """

    @staticmethod
    def add_package_nodes(trace_dataset: TraceDataset, package_artifact_type: str = DEFAULT_PACKAGE_ARTIFACT_TYPE) -> None:
        """
        Extracts packages and adds them as artifacts.
        :param trace_dataset: The trace dataset to add package nodes to.
        :param package_artifact_type: The artifact type to represent packages.
        :return: None (artifact data frame is modified)
        """
        artifact_ids = trace_dataset.artifact_df.index
        package_hierarchy, packages = PackageTracer._extract_package_hierarchy(artifact_ids)

        PackageTracer._add_package_artifacts(trace_dataset, packages, package_artifact_type)
        PackageTracer._add_package_links(trace_dataset, package_hierarchy)

    @staticmethod
    def _add_package_links(trace_dataset: TraceDataset, package_hierarchy: Dict[str, List[str]]) -> None:
        """
        Adds trace link package hierarchy to trace dataset. Layer data frame is updated along with trace links.
        :param trace_dataset: The trace dataset containing the package artifacts and the one to add the links to.
        :param package_hierarchy: The hierarchy of packages and source code files.
        :return: None (dataset is modified).
        """
        layer_ids = set()
        trace_ids = set()
        links = []

        for parent_node, children in package_hierarchy.items():
            for child_node in children:
                # Adds layer if missing
                parent_layer_id = trace_dataset.artifact_df.get_artifact(parent_node)[ArtifactKeys.LAYER_ID]
                child_layer_id = trace_dataset.artifact_df.get_artifact(child_node)[ArtifactKeys.LAYER_ID]
                layer_id = f"{parent_layer_id}2{child_layer_id}"
                if layer_id not in layer_ids:
                    trace_dataset.layer_df.add_layer(source_type=child_layer_id, target_type=parent_layer_id)
                    layer_ids.add(layer_id)

                # Adds trace link if not added
                trace_id = TraceDataFrame.generate_link_id(source_id=child_node, target_id=parent_node)
                if trace_id not in trace_ids:
                    trace_entry = Trace(
                        source=child_node,
                        target=parent_node,
                        label=1,
                        explanation=PACKAGE_EXPLANATION
                    )
                    links.append(trace_entry)
                    trace_ids.add(trace_id)
                else:
                    logger.info(f"Found duplicate package relationship: {parent_node} -> {child_node}")
        trace_dataset.trace_df.add_links(links)

    @staticmethod
    def _add_package_artifacts(trace_dataset: TraceDataset, packages: Iterable[str], package_artifact_type: str):
        """
        Adds the packages as artifacts to trace dataset.
        :param trace_dataset: The dataset to add the packages to.
        :param packages: List of package names to add.
        :param package_artifact_type: The artifact type of the package.
        :return: None (dataset is modified in place).
        """
        artifact_ids_set = set(trace_dataset.artifact_df.index)
        for package in packages:
            trace_dataset.artifact_df.add_artifact(id=package,
                                                   layer_id=package_artifact_type,
                                                   content=EMPTY_STRING,
                                                   summary=EMPTY_STRING)
            artifact_ids_set.add(package)

    @staticmethod
    def _extract_package_hierarchy(file_paths: List[str]) -> Tuple[Dict[str, List[str]], set[str]]:
        """
        Extracts the list of packages references in the list of file paths.
        :param file_paths: The file paths to source code.
        :return: List of unique packages.
        """
        package_set = set()
        package_hierarchy = {}
        for file_path in file_paths:
            file_packages = FileUtil.split_into_parts(file_path)
            for i in range(0, len(file_packages) - 1):
                parent_path = os.path.join(*file_packages[:i + 1])
                child_path = os.path.join(*file_packages[:i + 2])
                if parent_path not in package_hierarchy:
                    package_hierarchy[parent_path] = set()
                    package_set.add(parent_path)
                if child_path not in package_hierarchy[parent_path]:
                    package_hierarchy[parent_path].add(child_path)
                    package_set.add(child_path)

        package_hierarchy = {p: list(c) for p, c in package_hierarchy.items()}
        return package_hierarchy, package_set
