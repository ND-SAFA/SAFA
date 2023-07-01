import random
from typing import Callable, Dict, List

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.fake_project_reader import FakeProjectReader
from tgen.jobs.trainer_jobs.vsm_job import VSMJob
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.util.status import Status

GenericSorter = Callable[[List[str], List[str], Dict], List[str]]  # source names, target names, artifact map -> sorted target names


def alphabetical_sorter(source_names, target_names, artifact_map) -> Dict[str, List[str]]:
    target_names.sort()
    return {s: target_names for s in source_names}


def random_sorter(source_names, target_names, artifact_map) -> Dict[str, List[str]]:
    random.seed(42)
    random.shuffle(target_names)
    return {s: target_names for s in source_names}


def vsm_sorter(parent_names: List[str], child_names: List[str], artifact_map: Dict[str, str]) -> Dict[str, str]:
    parent_tag_name = "target"
    child_tag_name = "source"
    artifact_names = parent_names + child_names
    artifact_map = [artifact_map[a_name] for a_name in artifact_names]
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: artifact_names,
                                     ArtifactKeys.CONTENT: artifact_map,
                                     ArtifactKeys.LAYER_ID: [parent_tag_name for source in parent_names] +
                                                            [child_tag_name for target in child_names]})
    layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [child_tag_name], LayerKeys.TARGET_TYPE: [parent_tag_name]})
    dataset_creator = TraceDatasetCreator(FakeProjectReader(artifact_df=artifact_df, layer_df=layer_df))

    trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=dataset_creator)
    vsm_job = VSMJob(trainer_dataset_manager=trainer_dataset_manager)
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
        unsorted_targets[source][target] = entry["score"]
    sorted_targets = {source: sorted(targets2score, key=targets2score.get, reverse=True) for source, targets2score in
                      unsorted_targets.items()}
    return sorted_targets


DEFAULT_SORTING_PROMPT = "Rank the following artifacts from most to least " \
                         "important to the overall system functionality. " \
                         "Provide your answer as comma delimited list of artifact ids." \
                         "Enclose the list in <links></links>. "

registered_sorters: Dict[str, GenericSorter] = {
    "alphabetical": alphabetical_sorter,
    "random": random_sorter,
    "vsm": vsm_sorter
}
