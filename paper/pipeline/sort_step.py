from typing import Callable, Dict, List

from paper.common.completion_util import complete_prompts
from paper.common.ranking_prompt_builder import RankingPromptBuilder
from paper.pipeline.response_process_step import process_ranked_artifacts
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.fake_project_reader import FakeProjectReader
from tgen.jobs.trainer_jobs.vsm_job import VSMJob
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.util.status import Status

GenericSorter = Callable[[List[str], List[str], Dict], List[str]]  # source names, target names, artifact map -> sorted target names


def test_sorter(source_names, target_names, artifact_map) -> List[str]:
    target_names.sort()
    return target_names


def vsm_sorter(source_names, target_names, artifact_map) -> Dict[str, str]:
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: source_names + target_names,
                                     ArtifactKeys.CONTENT: list(artifact_map.values()),
                                     ArtifactKeys.LAYER_ID: ["source" for source in source_names] +
                                                            ["target" for target in target_names]})
    layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: ["source"], LayerKeys.TARGET_TYPE: ["target"]})
    dataset_creator = TraceDatasetCreator(FakeProjectReader(artifact_df=artifact_df, layer_df=layer_df))

    trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=dataset_creator)
    vsm_job = VSMJob(trainer_dataset_manager=trainer_dataset_manager)
    job_result = vsm_job.run()
    assert job_result.status == Status.SUCCESS, f"Sorting using VSM failed. {job_result.body}"
    vsm_result: TraceTrainOutput = job_result.body
    prediction_entries = vsm_result.prediction_output.prediction_entries
    unsorted_targets = {}
    for entry in prediction_entries:
        source = entry["source"]
        if source not in unsorted_targets:
            unsorted_targets[source] = {}
        unsorted_targets[source][entry["target"]] = entry["score"]
    sorted_targets = {source: sorted(targets2score, key=targets2score.get, reverse=True) for source, targets2score in
                      unsorted_targets.items()}
    return sorted_targets


DEFAULT_SORTING_PROMPT = "Rank the following artifacts from most to least " \
                         "important to the overall system functionality. " \
                         "Provide the ranked artifacts as comma delimited list of artifact ids."


def claude_sorter(source_names: List[str], target_names, artifact_map) -> List[str]:
    builder = RankingPromptBuilder()
    builder.with_task(DEFAULT_SORTING_PROMPT)
    for t_name in target_names:
        builder.with_artifact(t_name, artifact_map[t_name])
    prompt = builder.get()
    model = "claude-v1.3-100k"  # "claude-v1.3-100k", "claude-instant-v1-100k"
    batch_response = complete_prompts([prompt], model=model, max_tokens=600)
    batch_ranked_target_artifacts = process_ranked_artifacts(batch_response, target_names)
    sorted_target_artifacts = batch_ranked_target_artifacts[0]

    source2target = {}

    for s in source_names:
        source2target[s] = sorted_target_artifacts
    return source2target


registered_sorters: Dict[str, GenericSorter] = {
    "test": test_sorter,
    "claude": claude_sorter,
    "vsm": vsm_sorter
}
