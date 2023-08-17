import uuid

from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.status import Status
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import get_initials
from tgen.jobs.components.job_result import JobResult
from tgen.testres.paths.paths import TEST_HGEN_PATH


class HGenTestConstants:
    description = "A User story is a concise, informal description of a software feature or functionality, " \
                  "written from the perspective of the end user"
    example = "As a frequent traveler, I want to be able to filter hotel search results by distance " \
              "so that I can find accommodations close to my desired location."
    format_ = "As a [type of user], I want to [action or goal] so that [reason or benefit]."
    questions = "What are the main classes/functions in the code?\n" \
                "What are the inputs and outputs of the main functions?\n" \
                "Is there any user interface code and what does it do?"
    responses_inputs = [PromptUtil.create_xml("questions", questions)]
    open_ai_responses = [f'{PromptUtil.create_xml("description", description)}'
                         f'{PromptUtil.create_xml("example", example)} '
                         f'{PromptUtil.create_xml("format", format_)}']
    summary = "Here is a summary of the key technical details and design aspects of the system based on the provided code"

    user_stories = ["As a player, I want to move around in a 3D world so that I can explore the environment.",
                    "As a player, I want to place and remove blocks in the world so that I can modify the environment.",
                    "As a player, I want to copy the color of blocks so that I can reuse colors while building."]


def get_generated_artifacts_response(contents=None, type_="user-story"):
    if contents is None:
        contents = HGenTestConstants.user_stories
    response = PromptUtil.create_xml("summary", HGenTestConstants.summary)
    for us in contents:
        response += PromptUtil.create_xml(type_, us)
    return [response]


def get_name_responses(generated_artifact_content=None, target_type="User Story"):
    if not generated_artifact_content:
        generated_artifact_content = HGenTestConstants.user_stories
    names = [f"{i}" for i, _ in enumerate(generated_artifact_content)]
    expected_names = [f"{name} {get_initials(target_type)}" for name in names]
    return names, expected_names, [PromptUtil.create_xml("title", name) for name in names]


def get_ranking_job_result(expected_names, source_artifact_names):
    prediction_entries = [{"source": source, "target": target, "score": 0.8, "label": 1, "explanation": "explanation"}
                          for target in expected_names
                          for source in source_artifact_names]
    job_result = JobResult(status=Status.SUCCESS,
                           body=TracePredictionOutput(prediction_entries=prediction_entries),
                           job_id=uuid.uuid4())
    return job_result


def get_all_responses(content=None, target_type=None):
    if content is None:
        content = HGenTestConstants.user_stories
    step2 = HGenTestConstants.responses_inputs
    type_ = "-".join(target_type.lower().split())
    step3 = get_generated_artifacts_response(contents=content, type_=type_)
    step4 = get_name_responses(generated_artifact_content=content, target_type=target_type)
    return step4[1], step2 + step3 + step4[-1]


def get_test_hgen_args():
    return HGenArgs(source_layer_id="C++ Code",
                    target_type="Test User Story",
                    dataset_creator_for_sources=PromptDatasetCreator(
                        trace_dataset_creator=TraceDatasetCreator(DataFrameProjectReader(project_path=TEST_HGEN_PATH))))
