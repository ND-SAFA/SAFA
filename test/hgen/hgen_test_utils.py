import uuid
from copy import deepcopy

from tgen.common.constants.deliminator_constants import COMMA
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

    user_stories = ["As a game developer, I want a Player class to store player state, apply movement, "
                    "handle collisions, perform raycasting for block selection, and render the player, "
                    "so that I can implement a controllable character that interacts with the 3D world.",
                    "As a game developer, I want a RenderEngine class to handle window creation, OpenGL "
                    "context, camera view, and scene rendering, so that I have a reusable graphics "
                    "engine for displaying 3D scenes.",
                    "As a game developer, I want an Image class to load image files as textures using "
                    "STB Image, so that I can apply detailed textures to 3D models."]
    code_files = [["/Player.cpp"], ["/Rendering/RenderEngine.cpp"], ["/Rendering/Image.cpp", "/Rendering/stb_image.cpp"]]


def get_generated_artifacts_response(contents=None, sources=None, target_type="user-story", source_type="code"):
    if contents is None:
        contents = HGenTestConstants.user_stories
    if sources is None:
        sources = HGenTestConstants.code_files
    contents = deepcopy(contents)
    for i, content in enumerate(contents):
        source = sources[i % len(HGenTestConstants.code_files)]
        content += PromptUtil.create_xml(source_type, COMMA.join(source))
        contents[i] = content
    response = PromptUtil.create_xml("summary", HGenTestConstants.summary)
    for us in contents:
        response += PromptUtil.create_xml(target_type, us)
    return [response]


def get_name_responses(generated_artifact_content=None, target_type="User Story"):
    if not generated_artifact_content:
        generated_artifact_content = HGenTestConstants.user_stories
    if isinstance(generated_artifact_content, dict):
        generated_artifact_content = generated_artifact_content.keys()
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


def get_all_responses(content=None, target_type="User Story", sources=None, source_type="code"):
    step2 = HGenTestConstants.responses_inputs
    target_type_tag = "-".join(target_type.lower().split())
    source_type_tag = "-".join(source_type.lower().split())
    step3 = get_generated_artifacts_response(contents=content, target_type=target_type_tag, sources=sources,
                                             source_type=source_type_tag)
    step4 = get_name_responses(generated_artifact_content=content, target_type=target_type)
    return step4[1], step2 + step3 + step4[-1]


def get_test_hgen_args():
    return lambda: HGenArgs(source_layer_id="C++ Code",
                            target_type="Test User Story",
                            dataset_creator_for_sources=PromptDatasetCreator(
                                trace_dataset_creator=TraceDatasetCreator(DataFrameProjectReader(project_path=TEST_HGEN_PATH))))
