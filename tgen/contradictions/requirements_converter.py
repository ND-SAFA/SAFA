from typing import List, Dict, Any

from tgen.common.constants.model_constants import get_best_default_llm_manager_short_context
from tgen.common.logging.logger_manager import logger
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.with_decision_tree.requirement import Requirement, RequirementConstituent
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.contradiction_prompts import CONSTITUENT2TAG
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class RequirementsConverter:

    def __init__(self, llm_manager: AbstractLLMManager = None, export_path: str = None):
        """
        Responsible for converting an artifact to the expected format for requirements.
        :param llm_manager: The LLM to use for the constituent extraction from the artifact.
        :param export_path: Where to export responses to.
        """
        self.llm_manager = llm_manager if llm_manager else get_best_default_llm_manager_short_context()
        self.export_path = export_path

    def convert_artifacts(self, artifacts: List[Artifact]) -> List[Requirement]:
        """
        Converts a list of artifacts to a list using the requirements format.
        :param artifacts: A list of artifacts.
        :return: The artifacts converted to the requirements format.
        """
        dataset = PromptDataset(artifact_df=ArtifactDataFrame(artifacts))
        task_prompt = SupportedPrompts.REQUIREMENT_EXTRACT_CONSTITUENTS.value
        prompt_builder = PromptBuilder([ArtifactPrompt(prompt_args=PromptArgs(f"{PromptUtil.as_markdown_header('REQUIREMENT')}\n"),
                                                       include_id=False, build_method=ArtifactPrompt.BuildMethod.BASE),
                                        task_prompt])
        trainer_state = LLMTrainerState(prompt_builders=prompt_builder,
                                        trainer_dataset_manager=TrainerDatasetManager.create_from_datasets(eval=dataset),
                                        llm_manager=self.llm_manager)
        trainer = LLMTrainer(trainer_state)
        res = trainer.perform_prediction(save_and_load_path=FileUtil.safely_join_paths(self.export_path,
                                                                                       "artifact2requirement_response.yaml"))
        requirements = [self._create_requirement(r[task_prompt.args.prompt_id], art[ArtifactKeys.ID]) for art, r in
                        zip(artifacts, res.predictions)]
        return requirements

    @staticmethod
    def _create_requirement(res_dict: Dict[str, list], req_id: str) -> Requirement:
        """
        Creates a requirement from the LLM response.
        :param res_dict: Contains the tags mapped to their response.
        :param req_id: The id of the requirement.
        :return:  A requirement created from the LLM response.
        """
        params = {"id": req_id}
        for constituent in RequirementConstituent:
            tag = CONSTITUENT2TAG.get(constituent)
            if isinstance(tag, dict):
                params[constituent.value] = {sub_constituent: RequirementsConverter._get_res_value(res_dict, t)
                                             for sub_constituent, t in tag.items()}
            else:
                params[constituent.value] = RequirementsConverter._get_res_value(res_dict, tag)
        requirement = Requirement(**params)
        if requirement.is_empty():
            logger.error(f"!!Failed to convert artifact to requirement {req_id} - bad response!!")
        return requirement

    @staticmethod
    def _get_res_value(res_dict: Dict, value_tag: str) -> Any:
        """
        Gets the value from the response.
        :param res_dict: Contains the tags mapped to response.
        :param value_tag: The tag associated with the value.
        :return: The value.
        """
        value = res_dict.get(value_tag)
        if len(value) > 0:
            value = value[0]
        return value
