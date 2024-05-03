from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.with_decision_tree.requirement import Requirement, RequirementConstituent
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.supported_prompts.contradiction_prompts import CONSTITUENT2TAG

R1 = Requirement(id="1",
                 action={RequirementConstituent.EFFECT: "stand",
                         RequirementConstituent.CONDITION: "rains"},
                 variable={RequirementConstituent.EFFECT: "The car",
                           RequirementConstituent.CONDITION: "it"},
                 condition="when it rains",
                 effect="the car must stand")
R2 = Requirement(id="2",
                 action={RequirementConstituent.EFFECT: "drive",
                         RequirementConstituent.CONDITION: "rains"},
                 variable={RequirementConstituent.EFFECT: "car",
                           RequirementConstituent.CONDITION: "it"},
                 condition="when it rains",
                 effect="the car must drive")
R3 = Requirement(id="3",
                 action={RequirementConstituent.EFFECT: "stand"},
                 variable={RequirementConstituent.EFFECT: "The vehicle"},
                 effect="the vehicle must stand",
                 condition="")
R4 = Requirement(id="4",
                 action={RequirementConstituent.EFFECT: "stand"},
                 variable={RequirementConstituent.EFFECT: "The conductor"},
                 effect="the conductor must stand",
                 condition="when it snows")
R5 = Requirement(id="5",
                 action={RequirementConstituent.EFFECT: "stand"},
                 variable={RequirementConstituent.EFFECT: "The Conductor"},
                 effect="the conductor must sit",
                 condition="when its a blizzard")
REQUIREMENTS = [R1, R2, R3, R4, R5]
LAYER_ID = "requirement"
EXPECTED_CONTRADICTIONS = {"2": ["1"]}


def get_response_for_req(requirement: Requirement):
    responses = [PromptUtil.create_xml(tag, requirement.get_constituent(constituent)) for constituent, tag in CONSTITUENT2TAG.items()
                 if isinstance(tag, str)]
    responses.extend([PromptUtil.create_xml(tag, requirement.get_constituent(component, constituent=constituent))
                      for component, tags in CONSTITUENT2TAG.items() if isinstance(tags, dict)
                      for constituent, tag in tags.items()])
    return NEW_LINE.join(responses)


def get_artifact_content(requirement: Requirement):
    return f"{requirement.get_condition()}, {requirement.get_effect()}"


def get_contradictions_dataset() -> PromptDataset:
    content = [get_artifact_content(r) for r in REQUIREMENTS]
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [str(i + 1) for i in range(len(content))],
                                     ArtifactKeys.CONTENT: content,
                                     ArtifactKeys.LAYER_ID: [LAYER_ID for _ in range(len(content))]})
    trace_dataset = TraceDataset(artifact_df, TraceDataFrame(), LayerDataFrame({LayerKeys.SOURCE_TYPE: [LAYER_ID],
                                                                                LayerKeys.TARGET_TYPE: [LAYER_ID]}))
    return PromptDataset(trace_dataset=trace_dataset)
