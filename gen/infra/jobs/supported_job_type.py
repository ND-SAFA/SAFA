from gen_common.clustering.clustering_job import ClusteringJob
from gen_common.summarize.jobs.summarize_job import SummarizeJob
from gen_common.traceability.ranking.job import RankingJob
from gen_common.traceability.vsm.vsm_job import VSMJob
from gen_common.util.supported_enum import SupportedEnum

from gen.chat.chat_job import ChatJob
from gen.data.jobs.create_datasets_job import CreateDatasetsJob
from gen.data.jobs.create_source_splits_job import CreateSourceSplitsJob
from gen.data.jobs.download_repository_job import DownloadRepositoryJob
from gen.data.jobs.export_artifacts_job import ExportArtifactsJob
from gen.delta.delta_summarizer_job import DeltaSummarizerJob
from gen.health.health_job import HealthCheckJob
from gen.hgen.jobs.base_hgen_job import BaseHGenJob
from gen.hgen.jobs.multi_layer_hgen_job import MultiLayerHGenJob
from gen.tracing.jobs.code_trace_job import TraceCodeJob
from gen.tracing.jobs.ranking_chunk_job import RankingChunkJob
from gen.tracing.jobs.tracing_job import TracingJob


class SupportedJobType(SupportedEnum):
    HGEN = BaseHGenJob
    SUMMARY = SummarizeJob
    MULTI_LAYER_HGEN = MultiLayerHGenJob
    EXPORT_ARTIFACTS = ExportArtifactsJob
    CREATE_DATASETS = CreateDatasetsJob
    DELTA = DeltaSummarizerJob
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
