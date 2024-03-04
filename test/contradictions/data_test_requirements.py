from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.requirement import Requirement, RequirementConstituent
from tgen.prompts.supported_prompts.requirements_contradiction_prompts import CONSTITUENT2TAG

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


def get_response_for_req(requirement: Requirement):
    responses = [PromptUtil.create_xml(tag, requirement.get_constituent(constituent)) for constituent, tag in CONSTITUENT2TAG.items()
                 if isinstance(tag, str)]
    responses.extend([PromptUtil.create_xml(tag, requirement.get_constituent(component, constituent=constituent))
                      for component, tags in CONSTITUENT2TAG.items() if isinstance(tags, dict)
                      for constituent, tag in tags.items()])
    return NEW_LINE.join(responses)


def get_artifact_content(requirement: Requirement):
    return f"{requirement.get_condition()}, {requirement.get_effect()}"
