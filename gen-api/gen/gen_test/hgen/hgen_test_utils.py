from copy import deepcopy

from gen_common.constants.symbol_constants import COMMA
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.readers.dataframe_project_reader import DataFrameProjectReader
from gen_common.util.prompt_util import PromptUtil
from gen_common_test.base.mock.responses.summary import TEST_PROJECT_SUMMARY

from gen.hgen.common.hgen_util import HGenUtil
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hierarchy_generator import HierarchyGenerator
from gen_test.res.paths import GEN_TEST_PROJECT_HGEN_PATH


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
    n_reruns = 2


def get_generated_artifacts_response(contents=None, sources=None, target_type="user-story", source_type="code",
                                     use_clustering: bool = False):
    if contents is None:
        contents = HGenTestConstants.user_stories
    if sources is None:
        sources = HGenTestConstants.code_files
    contents = deepcopy(contents)
    if not use_clustering:
        for i, content in enumerate(contents):
            source = sources[i % len(sources)]
            content += PromptUtil.create_xml("ids", COMMA.join(source))
            contents[i] = content
        response = ""
        for us in contents:
            response += PromptUtil.create_xml(target_type, us)
        responses = [response]
    else:
        responses = [PromptUtil.create_xml(target_type, us) for us in contents]

    return responses


def get_name_responses(generated_artifact_content=None, target_type="User Story"):
    if not generated_artifact_content:
        generated_artifact_content = HGenTestConstants.user_stories
    if isinstance(generated_artifact_content, dict):
        generated_artifact_content = generated_artifact_content.keys()
    n_generated = sum([max(a.count(HGenUtil.convert_spaces_to_dashes(target_type)), 2) for a in generated_artifact_content]) / 2
    names = [f"{i}" for i in range(int(n_generated))]
    expected_names = [HGenUtil.format_names(name, target_type, i) for i, name in enumerate(names)]
    return names, expected_names, [PromptUtil.create_xml("title", name) for name in names]


def get_predictions(expected_names, source_artifact_names):
    predictions = [[{"id": i, "score": 0.8, "explanation": "explanation"}
                    for i, source in enumerate(source_artifact_names)] for name in expected_names]
    return predictions


def get_all_responses(content=None, target_type="User Story", sources=None, source_type="code", use_clustering: bool = True):
    step2 = HGenTestConstants.responses_inputs
    target_type_tag = "-".join(target_type.lower().split())
    source_type_tag = "-".join(source_type.lower().split())
    step3 = get_generated_artifacts_response(contents=content, target_type=target_type_tag, sources=sources,
                                             source_type=source_type_tag, use_clustering=use_clustering)
    step4 = get_name_responses(generated_artifact_content=content, target_type=target_type)
    return step4[1], step2 + step3 + step4[-1]


def get_test_hgen_args(test_refinement: bool = False, test_clustering: bool = False):
    return lambda: HGenArgs(source_layer_ids=["C++ Code"],
                            target_type="Test User Story",
                            run_refinement=test_refinement,
                            perform_clustering=test_clustering,
                            dataset_creator=PromptDatasetCreator(
                                trace_dataset_creator=TraceDatasetCreator(
                                    DataFrameProjectReader(
                                        project_path=GEN_TEST_PROJECT_HGEN_PATH
                                    )
                                )
                            )
                            )


HGEN_PROJECT_SUMMARY = deepcopy(TEST_PROJECT_SUMMARY)
for section in list(HGEN_PROJECT_SUMMARY.keys()):
    if section not in HierarchyGenerator.PROJECT_SUMMARY_SECTIONS:
        HGEN_PROJECT_SUMMARY.pop(section)
