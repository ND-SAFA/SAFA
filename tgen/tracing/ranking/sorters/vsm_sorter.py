from typing import Callable, Dict, List

from tgen.common.util.status import Status
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.trainer_jobs.vsm_job import VSMJob

GenericSorter = Callable[
    [List[str], List[str], Dict], Dict[str, str]]  # source names, target names, artifact map -> sorted target names

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-roberta-large-v1"
DEFAULT_SEARCH_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def vsm_sorter(parent_ids: List[str], child_ids: List[str], artifact_map: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Ranks children artifacts from most to least similar to the parent.
    :param parent_ids: The parent ids.
    :param child_ids: The child ids to rank.
    :param artifact_map: The map of artifact ids to body.
    :return:
    """
    parent_tag_name = "target"
    child_tag_name = "source"
    artifact_names = parent_ids + child_ids
    artifact_map = [artifact_map[a_name] for a_name in artifact_names]
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: artifact_names,
                                     ArtifactKeys.CONTENT: artifact_map,
                                     ArtifactKeys.LAYER_ID: [parent_tag_name for source in parent_ids] +
                                                            [child_tag_name for target in child_ids]})
    layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [child_tag_name], LayerKeys.TARGET_TYPE: [parent_tag_name]})

    trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: TraceDataset(artifact_df=artifact_df,
                                                                                                         trace_df=TraceDataFrame(),
                                                                                                         layer_df=layer_df)})
    vsm_job = VSMJob(trainer_dataset_manager=trainer_dataset_manager, select_predictions=False)
    job_result = vsm_job.run()
    assert job_result.status == Status.SUCCESS, f"Sorting using VSM failed. {job_result.body}"
    vsm_result: TraceTrainOutput = job_result.body
    prediction_entries = vsm_result.prediction_output.prediction_entries
    unsorted_targets = {}
    for entry in prediction_entries:
        source = entry[parent_tag_name]
        target = entry[child_tag_name]
        if source not in unsorted_targets:
            unsorted_targets[source] = {}
        unsorted_targets[source][target] = entry[StructuredKeys.SCORE]
    sorted_targets = {source: sorted(targets2score, key=targets2score.get, reverse=True) for source, targets2score in
                      unsorted_targets.items()}
    return sorted_targets


