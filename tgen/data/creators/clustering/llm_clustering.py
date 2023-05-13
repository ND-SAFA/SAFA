from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import TokenLimitCalculator, ModelTokenLimits
from tgen.train.trainers.trainer_task import TrainerTask


class LLMClustering:

    @staticmethod
    def cluster(llm_manager: AbstractLLMManager, artifact_df: ArtifactDataFrame):
        content = NEW_LINE.join([f"{i}) {content}" for i, content in enumerate(artifact_df[ArtifactKeys.CONTENT])])
        prompt_creator = GenerationPromptCreator(llm_manager.prompt_args, SupportedPrompts.CLUSTERING)
        prompt = prompt_creator.create(content)[PromptKeys.PROMPT]

        # TODO handle this case in the future
        n_tokens = TokenLimitCalculator.estimate_num_tokens(prompt, llm_manager.llm_args.model)
        assert n_tokens <= ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model), "LLM Clustering is currently only " \
                                                                                                   "supported for models with token " \
                                                                                                   "limits greater than the combined" \
                                                                                                   "artifact content length."
        params = llm_manager.llm_args.to_params(TrainerTask.PREDICT, LLMCompletionType.GENERATION)
        res = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION, prompt=prompt, **params)
        return res
