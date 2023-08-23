import os
from typing import Callable, Dict, List

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from tgen.common.util.celerystatus import CeleryStatus
from tgen.constants import environment_constants
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
    assert job_result.status == CeleryStatus.SUCCESS, f"Sorting using VSM failed. {job_result.body}"
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


def embedding_sorter(parent_ids: List[str], child_ids: List[str], artifact_map: Dict[str, str],
                     model_name=DEFAULT_EMBEDDING_MODEL, return_scores: bool = False) -> Dict[str, str]:
    cache_dir = os.environ.get("HF_DATASETS_CACHE", None)
    if environment_constants.IS_TEST or not os.path.exists(cache_dir):
        cache_dir = None
    model = SentenceTransformer(model_name, cache_folder=cache_dir)

    children_bodies = [artifact_map[a_id] for a_id in child_ids]
    children_embeddings = model.encode(children_bodies)

    parent2rankings = {}
    for parent_id in tqdm(parent_ids, desc="Performing Ranking Via Embeddings"):
        parent_body = artifact_map[parent_id]
        parent_embedding = model.encode([parent_body])
        scores = cosine_similarity(parent_embedding, children_embeddings)[0]
        sorted_artifact_ids = [a for s, a in sorted(zip(scores, child_ids), reverse=True, key=lambda k: k[0])]
        if return_scores:
            parent2rankings[parent_id] = (sorted_artifact_ids, scores)
        else:
            parent2rankings[parent_id] = sorted_artifact_ids
    return parent2rankings


registered_sorters: Dict[str, GenericSorter] = {
    "vsm": vsm_sorter,
    "embedding": embedding_sorter
}
