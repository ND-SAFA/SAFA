from tgen.common.util.supported_enum import SupportedEnum
from tgen.jobs.chat_jobs.chat_job import ChatJob
from tgen.jobs.clustering_job.clustering_job import ClusteringJob
from tgen.jobs.data_jobs.create_datasets_job import CreateDatasetsJob
from tgen.jobs.data_jobs.create_source_splits_job import CreateSourceSplitsJob
from tgen.jobs.data_jobs.download_repository_job import DownloadRepositoryJob
from tgen.jobs.data_jobs.export_artifacts_job import ExportArtifactsJob
from tgen.jobs.delta_jobs.delta_summarizer_job import DeltaSummarizerJob
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob
from tgen.jobs.model_jobs.create_model_job import CreateModelJob
from tgen.jobs.model_jobs.delete_model_job import DeleteModelJob
from tgen.jobs.rag.eval_concept_tracing_job import EvalConceptTracingJob
from tgen.jobs.rag.eval_rag_job import EvalRagJob
from tgen.jobs.summary_jobs.summarize_job import SummarizeJob
from tgen.jobs.tracing_jobs.code_trace_job import TraceCodeJob
from tgen.jobs.tracing_jobs.ranking_chunk_job import RankingChunkJob
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.jobs.tracing_jobs.tracing_job import TracingJob
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.jobs.trainer_jobs.vsm_job import VSMJob


class SupportedJobType(SupportedEnum):
    HUGGING_FACE = HuggingFaceJob
    HGEN = BaseHGenJob
    SUMMARY = SummarizeJob
    MULTI_LAYER_HGEN = MultiLayerHGenJob
    EXPORT_ARTIFACTS = ExportArtifactsJob
    CREATE_DATASETS = CreateDatasetsJob
    CREATE_MODEL = CreateModelJob
    DELETE_MODEL = DeleteModelJob
    DELTA = DeltaSummarizerJob
    LLM = LLMJob
    TRACING = TracingJob
    RANKING = RankingJob
    RANKING_CHUNKS = RankingChunkJob
    TRACE_CODE = TraceCodeJob
    VSM = VSMJob
    DOWNLOAD_REPO = DownloadRepositoryJob
    CREATE_SOURCE_SPLITS = CreateSourceSplitsJob
    CLUSTERING = ClusteringJob
    HEALTH_CHECK = HealthCheckJob
    CHAT = ChatJob
    EVAL_RAG = EvalRagJob
    EVAL_CONCEPT_TRACING = EvalConceptTracingJob
