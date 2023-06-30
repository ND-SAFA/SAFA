import os.path
import uuid

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.ranking.pipeline.base import DatasetIdentifier, RankingPipeline, RankingStore, get_trace_id
from tgen.ranking.pipeline.classification_step import compute_precision
from tgen.ranking.pipeline.map_step import calculate_map_instructions, compute_map
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.util.status import Status


def run_prediction_job(s: RankingStore):
    model = "claude-instant-v1-100k"
    job_args = JobArgs(output_dir=s.export_path)
    llm_args = AnthropicArgs(model=model)
    llm_manager = AnthropicManager(llm_args=llm_args)
    project_reader = StructuredProjectReader(project_path=s.project_path)
    dataset_creator = TraceDatasetCreator(project_reader=project_reader)
    trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=dataset_creator)

    job = LLMJob(trainer_dataset_manager=trainer_dataset_manager, llm_manager=llm_manager, job_args=job_args)
    job_result = job.run()
    if job_result.status == Status.FAILURE:
        raise Exception(job_result.body)
    s.job_result = job_result
    prediction_output: TracePredictionOutput = job_result.body

    t_preds = {}
    traced_ids = set()
    for entry in prediction_output.prediction_entries:
        source = entry["source"]
        target = entry["target"]
        score = entry["score"]
        label = entry["label"]

        if label == 1:
            traced_ids.add(get_trace_id(entry))

        if source not in t_preds:
            t_preds[source] = []
        t_preds[source].append({"name": target, "score": score, "label": label})

    source_ids = list(t_preds.keys())
    predicted_target_links = []
    for source in source_ids:
        targets = t_preds[source]
        sorted_targets = sorted(targets, key=lambda d: d["score"], reverse=True)
        sorted_targets = list(map(lambda t: t["name"], sorted_targets))
        predicted_target_links.append(sorted_targets)

    map_instructions = calculate_map_instructions(predicted_target_links, source_ids, list(traced_ids))
    s.map_instructions = map_instructions
    s.source_ids = source_ids


if __name__ == "__main__":
    EXPERIMENT_ID = str(uuid.uuid4())
    DATASET_NAME = "cm1"
    dataset_path = f"~/desktop/safa/datasets/paper/{DATASET_NAME}"
    dataset_path = os.path.expanduser(dataset_path)

    dataset_id = DatasetIdentifier(dataset_path=dataset_path, experiment_id=EXPERIMENT_ID, dataset_name=DATASET_NAME)

    steps = [run_prediction_job,
             compute_map,
             compute_precision]
    pipeline = RankingPipeline(dataset_id, steps)
    pipeline.run()
