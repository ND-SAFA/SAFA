import os
from typing import Dict, List, Tuple

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.tracing.code_tracer_constants import DEFAULT_PACKAGE_ARTIFACT_TYPE, PACKAGE_EXPLANATION
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset


class PackageTracer:
    """
    Creates package nodes from source code.
    - Add package artifacts
    - Add links from packages to code artifacts
    - (Optional) Migrates links between source code and other artifacts to the packages of the source codes
    """

    @staticmethod
    def add_package_nodes(trace_dataset: TraceDataset, package_type: str = DEFAULT_PACKAGE_ARTIFACT_TYPE) -> None:
        """
        Extracts packages and adds them as artifacts.
        :return: None (artifact data frame is modified)
        """
        artifact_ids = trace_dataset.artifact_df.index
        original_artifact_types = trace_dataset.artifact_df[ArtifactKeys.LAYER_ID.value].unique()

        PackageTracer._add_packages_as_artifacts(trace_dataset, package_type)
        trace_dataset.layer_df.add_layer(source_type=package_type, target_type=package_type)
        for original_artifact_type in original_artifact_types:
            trace_dataset.layer_df.add_layer(source_type=original_artifact_type, target_type=package_type)

    @staticmethod
    def _add_packages_as_artifacts(trace_dataset: TraceDataset, package_artifact_type=DEFAULT_PACKAGE_ARTIFACT_TYPE):
        """
        Adds code packages as artifacts to trace dataset.
        :param package_artifact_type: The artifact type for the packages.
        :param trace_dataset: The dataset to modify.
        :return: None (dataset is modified in place).
        """
        artifact_ids = trace_dataset.artifact_df.index
        package_hierarchy, packages = PackageTracer._extract_package_hierarchy(artifact_ids)

        links = []
        trace_ids = set()
        artifact_ids_set = set(artifact_ids)

        for package in packages:
            trace_dataset.artifact_df.add_artifact(artifact_id=package,
                                                   layer_id=package_artifact_type,
                                                   content=EMPTY_STRING,
                                                   summary=EMPTY_STRING)
            artifact_ids_set.add(package)

        for parent_node, children in package_hierarchy.items():
            for child_node in children:
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
        trace_dataset.trace_df.add_links(links)

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
