import os.path
from typing import List

import numpy as np

from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.scripts.tools.htrace.embedding_tracer import embedding_tracer
from tgen.scripts.tools.htrace.types import TracerMethodType
from tgen.scripts.tools.htrace.vsm_tracer import vsm_tracer
from tgen.summarizer.summary import SummarySectionKeys

stopwords = ["where", "is", "the", "to"]
name2method = {
    "embedding": embedding_tracer,
    "vsm": vsm_tracer
}


def main(project_path: str):
    use_docs = True
    project_reader = StructuredProjectReader(project_path)
    trace_dataset_creator = TraceDatasetCreator(project_reader=project_reader)
    prompt_dataset_creator = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator)
    prompt_dataset = prompt_dataset_creator.create()
    trace_dataset = prompt_dataset.trace_dataset
    create_project_summary(project_path, prompt_dataset)

    question = "Where is the request to waze being sent?"  # input("Question:")
    layer_direction = ["Entry Point", "Sub-System", "Code"] if use_docs else ["Class"]
    starting_artifacts = trace_dataset.artifact_df.get_artifacts_by_type(layer_direction[0]).to_artifacts()
    tracing_method = name2method["vsm"]
    selected_artifacts = run_selective_tracing(trace_dataset, starting_artifacts, layer_direction, question, tracing_method)
    selected_artifact_path = [a["id"] for a_batch in selected_artifacts for a in a_batch]
    print(selected_artifacts)


def run_selective_tracing(trace_dataset: TraceDataset,
                          starting_artifacts: List[Artifact],
                          layer_direction: List[str],
                          question: str,
                          tracing_method: TracerMethodType):
    question_chunks = [w for w in question.split(" ") if w not in stopwords]
    artifact_to_embedd = question_chunks

    target_class = layer_direction[-1]
    curr_index = 0
    next_layer = layer_direction[curr_index + 1]
    running = True
    selected_path = [starting_artifacts]
    state = {}
    while running:
        target_artifacts_ids = set()
        for artifact in starting_artifacts:
            artifact_children = trace_dataset.trace_df.get_children(artifact[ArtifactKeys.ID])
            target_artifacts_ids.update(artifact_children)
        target_artifacts = [trace_dataset.artifact_df.get_artifact(a_id) for a_id in target_artifacts_ids]
        target_artifacts = [a for a in target_artifacts if a[ArtifactKeys.LAYER_ID] == next_layer]
        target_artifact_bodies = [a["summary"] for a in target_artifacts]
        similarity_matrix = tracing_method(state, question_chunks, target_artifact_bodies)
        starting_artifacts = select_next_artifacts(target_artifacts, similarity_matrix)
        selected_path.append(starting_artifacts)
        if any([a[ArtifactKeys.LAYER_ID] == target_class for a in starting_artifacts]):
            break
        curr_index += 1
        next_layer = layer_direction[curr_index + 1]
    return selected_path


def select_next_artifacts(layer_artifacts, similarity_matrix):
    selected_artifacts_items = []
    for i in range(similarity_matrix.shape[0]):
        similarity_scores = similarity_matrix[i].tolist()
        sorted_artifacts = [x for x in sorted(zip(layer_artifacts, similarity_scores), key=lambda x: x[1], reverse=True)]
        selected_artifacts_items.append(sorted_artifacts[0])
    selected_artifacts_items = sorted(selected_artifacts_items, key=lambda x: x[1], reverse=True)
    selected_artifacts = [x[0] for x in selected_artifacts_items]
    return selected_artifacts


def get_content(a):
    summary = a[ArtifactKeys.SUMMARY]
    if isinstance(summary, float) and np.isnan(summary):
        return a[ArtifactKeys.CONTENT]
    return summary


def create_project_summary(project_path: str, prompt_dataset: PromptDataset):
    trace_dataset = prompt_dataset.trace_dataset
    project_summary = prompt_dataset.project_summary
    project_summary_sections = ["Overview"]
    layer_to_doc = ["Entry Point", "Sub-System"]
    readme = ""

    for prompt_summary_section in project_summary_sections:
        section_content = project_summary[prompt_summary_section][SummarySectionKeys.CHUNKS][0]
        readme += f"# {prompt_summary_section}\n{section_content}\n\n"

    for layer in layer_to_doc:
        layer_artifacts = trace_dataset.artifact_df.get_artifacts_by_type(layer).to_artifacts()
        layer_artifact_content = ""
        for a in layer_artifacts:
            title = f"# {a[ArtifactKeys.ID]}"
            content = f"{a[ArtifactKeys.SUMMARY]}"
            layer_artifact_content += f"\n{title}\n{content}\n\n"
        layer_content = f"# {layer.title()}\n{layer_artifact_content}\n"
        readme += f"{layer_content}"

    readme = readme.strip()
    FileUtil.write(readme, os.path.join(project_path, "README.md"))


if __name__ == "__main__":
    PROJECT_PATH = os.path.expanduser("~/desktop/safa/datasets/waze-api/ss/summarized")
    main(PROJECT_PATH)
