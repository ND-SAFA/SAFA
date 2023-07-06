from typing import Dict, List, Union

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class TracingJob(AbstractJob):
    """
    Performs filtering with little claude before ranking with big claude.
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL,
                 select_top_predictions: bool = True):
        """
        Constructs job for dataset at given role.
        :param trainer_dataset_manager: The manager containing all datasets.
        :param dataset_role: The role to predict links for.
        """
        super().__init__()
        self.trainer_dataset_manager = trainer_dataset_manager
        self.dataset_role = dataset_role
        self.llm_args = AnthropicArgs(model="claude-instant-v1", temperature=0)
        self.llm_manager = AnthropicManager(llm_args=self.llm_args)
        self.dataset_role = dataset_role
        self.select_top_predictions = select_top_predictions

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Filters and ranks links with little claude then ranks with big claude.
        :param kwargs: Any keyword arguments.
        :return: The trace output.
        """
        THRESHOLD = 0.5
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = DataStructureUtil.create_artifact_map(dataset.artifact_df)

        base_tracing_job = LLMJob(self.trainer_dataset_manager, task=TrainerTask.PREDICT, llm_manager=self.llm_manager)
        prediction_output: TracePredictionOutput = base_tracing_job.run().body

        entries = prediction_output.prediction_entries
        entries = [entry for entry in entries if entry["score"] >= THRESHOLD]

        parent2entries: Dict[str, List[TracePredictionEntry]] = self.create_id_to_entries(entries, "target")
        parent_ids = list(parent2entries.keys())
        parent2children: Dict[str, List[str]] = {target: [t["source"] for t in entries] for target, entries in parent2entries.items()}

        parent2rankings = RankingUtil.rank_children(parent_ids, parent2children, artifact_map)

        predicted_entries = []

        for parent_id, ranked_sources in parent2rankings.items():
            target_entries = parent2entries[parent_id]
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_sources, target_entries)
            predicted_entries.extend(target_predicted_entries)
        if self.select_top_predictions:
            predicted_entries = RankingUtil.select_predictions(predicted_entries)
        RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def create_id_to_entries(entries, artifact_key: str):
        """
        Groups entries by key given.
        :param entries: The entries to group.
        :param artifact_key: The key to group by.
        :return: Map of key value to entries.
        """
        id2entries: Dict[str, List[Dict]] = {}
        for entry in entries:
            artifact_id = entry[artifact_key]
            if artifact_id not in id2entries:
                id2entries[artifact_id] = []
            id2entries[artifact_id].append(entry)

        id2entries = {t_id: sorted(entries, key=lambda t: t["score"], reverse=True) for t_id, entries in id2entries.items()}
        return id2entries
