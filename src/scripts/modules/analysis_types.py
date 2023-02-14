from typing import Dict, List, TypedDict


class LinkMetrics(TypedDict):
    """
    The metrics calculated for a link.
    """
    artifact_tokens: List[str]
    link_true_label: int
    analysis: Dict
    categories: List[str]


LinkCollectionAnalysis = Dict[str, LinkMetrics]
JobCollection = Dict[str, Dict[int, List[str]]]


class JobSummaryMetrics(TypedDict):
    """
    The summary metrics for a job predictions.
    """
    mis_predicted_n_per_category: Dict
    correctly_predicted_n_per_category: Dict


class JobAnalysis(TypedDict):
    """
    The analysis of a job's predicted links.
    """
    summary: JobSummaryMetrics
    mis_link_collection: LinkCollectionAnalysis
    correct_link_collection: LinkCollectionAnalysis


class MultiJobAnalysis(TypedDict):
    """
    Represents the analysis collected across multiple jobs from one or more scripts.
    """
    jobs: JobCollection
    job_analysis: Dict[str, JobAnalysis]
    intersections: Dict[str, Dict[int, List[int]]]
