from typing import Dict, List, Union

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.anthropic_args import AnthropicArgs, AnthropicParams
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.train.trainers.trainer_task import TrainerTask


class TracingJob(LLMJob):
    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL):
        super().__init__(trainer_dataset_manager, task=TrainerTask.PREDICT)
        self.dataset_role = dataset_role

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = self.create_artifact_map(dataset)

        prediction_output: TracePredictionOutput = super()._run(**kwargs)
        entries = prediction_output.prediction_entries

        source2entries: Dict[str, List[TracePredictionEntry]] = self.create_source_to_entries(entries)
        prompts, sources = self.create_ranking_prompts(artifact_map, source2entries)

        llm_manager = AnthropicManager(llm_args=AnthropicArgs(model="claude-v1.3-100k"))
        args = {AnthropicParams.PROMPT: prompts}
        completion_responses: GenerationResponse = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                                       **args)

        predicted_entries = []
        for i, response in enumerate(completion_responses.batch_responses):
            source = sources[i]
            source_predicted_entries = self.parse_ranking_response(source, response, source2entries)
            predicted_entries.extend(source_predicted_entries)

        metrics_manager = MetricsManager(trace_predictions=predicted_entries)
        metrics = list(SupportedTraceMetric.get_keys())
        metrics = metrics_manager.eval(metrics)
        print("Metrics")
        print(metrics)
        print()
        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def create_artifact_map(dataset):
        artifact_map = {}
        for i, artifact_row in dataset.artifact_df.iterrows():
            artifact_map[artifact_row.index] = artifact_row[ArtifactKeys.CONTENT.value]
        return artifact_map

    @staticmethod
    def parse_ranking_response(source, r, source2entries):
        source_entries = source2entries[source]
        source_target_ids = [t["target"] for t in source_entries]
        target2labels = {entry["target"]: entry["label"] for entry in source_entries}
        ranked_target_ids = TracingJob.parse_target_ids(r, source_target_ids)
        scores = TracingJob.assign_scores_to_targets(ranked_target_ids)
        source_predicted_entries = []
        for target, score in zip(ranked_target_ids, scores):
            entry = {
                "source": source,
                "target": target,
                "score": score,
                "label": target2labels[target]
            }
            source_predicted_entries.append(entry)
        return source_predicted_entries

    @staticmethod
    def create_ranking_prompts(artifact_map, source2entries: Dict[str, List[TracePredictionEntry]]):
        sources = []
        prompts = []
        for source, source_predicted_entries in source2entries.items():
            source_predicted_entries = sorted(source_predicted_entries, key=lambda t: t["score"], reverse=True)
            target_ids = [t["target"] for t in source_predicted_entries]
            prompt = TracingJob.format_ranking_prompt(source, target_ids, artifact_map)
            sources.append(source)
            prompts.append(prompt)
        return prompts, sources

    @staticmethod
    def create_source_to_entries(entries, threshold=0.5):
        source2entries: Dict[str, List[Dict]] = {}
        for entry in entries:
            source = entry["source"]
            target = entry["target"]
            score = entry["score"]
            if source not in source2entries:
                source2entries[source] = []
            if score >= threshold:
                source2entries[source].append(entry)
        return source2entries

    @staticmethod
    def assign_scores_to_targets(ranked_targets: List[str]):
        raise NotImplementedError()

    @staticmethod
    def parse_target_ids(r: str, all_targets: List[str]):
        raise NotImplementedError()

    @staticmethod
    def format_ranking_prompt(source: str, targets: List[str], artifact_map: Dict[str, str]):
        raise NotImplementedError()

    @staticmethod
    def format_targets(artifacts: List[str], artifact_map: Dict[str, str]):
        raise NotImplementedError()
