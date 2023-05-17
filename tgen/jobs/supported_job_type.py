from tgen.jobs.data_jobs.create_datasets_job import CreateDatasetsJob
from tgen.jobs.data_jobs.create_source_splits_job import CreateSourceSplitsJob
from tgen.jobs.data_jobs.download_repository_job import DownloadRepositoryJob
from tgen.jobs.data_jobs.export_artifacts_job import ExportArtifactsJob
from tgen.jobs.hgen_jobs.artifact_generator_job import GenerateArtifactsJob
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.model_jobs.create_model_job import CreateModelJob
from tgen.jobs.model_jobs.delete_model_job import DeleteModelJob
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.jobs.trainer_jobs.vsm_job import VSMJob
from tgen.util.supported_enum import SupportedEnum


class SupportedJobType(SupportedEnum):
    HUGGING_FACE = HuggingFaceJob
    HGEN = BaseHGenJob
    EXPORT_ARTIFACTS = ExportArtifactsJob
    CREATE_DATASETS = CreateDatasetsJob
    GENERATE_ARTIFACTS = GenerateArtifactsJob
    CREATE_MODEL = CreateModelJob
    DELETE_MODEL = DeleteModelJob
    LLM = LLMJob
    VSM = VSMJob
    DOWNLOAD_REPO = DownloadRepositoryJob
    CREATE_SOURCE_SPLITS = CreateSourceSplitsJob
