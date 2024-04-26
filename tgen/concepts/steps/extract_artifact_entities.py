from tgen.common.objects.artifact import Artifact
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.util.prompt_prediction import predict_artifact_prompt
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager


class EntityExtraction(AbstractPipelineStep):
    ENTITY_TAG = "entity"
    ENTITY_NAME_TAG = "name"
    ENTITY_DESCRIPTION_TAG = "desc"

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Extracts the most important entities from the target artifact.
        :param args:
        :param state:
        :return:
        """

        artifact_content = args.artifact[ArtifactKeys.CONTENT]
        llm_manager = OpenAIManager()
        instructions_prompt = Prompt("Above is an artifact from a software system. "
                                     "Please extract the acronyms used in the artifact. "
                                     "Attempt to define each acronym in the artifact. "
                                     f"Enclose each acronym within "
                                     f"<{self.ENTITY_TAG}>"
                                     f"<{self.ENTITY_NAME_TAG}>[ACRONYM]</{self.ENTITY_NAME_TAG}>"
                                     f"<{self.ENTITY_DESCRIPTION_TAG}>[DEFINITION]</{self.ENTITY_DESCRIPTION_TAG}>"
                                     f"</{self.ENTITY_TAG}>",
                                     title="\n\nInstructions",
                                     response_manager=PromptResponseManager(
                                         response_tag={self.ENTITY_TAG: [self.ENTITY_NAME_TAG, self.ENTITY_DESCRIPTION_TAG]}))
        response_dict = predict_artifact_prompt(artifact_content, instructions_prompt, llm_manager)

        entities = []
        for entity_dict in response_dict[self.ENTITY_TAG]:
            entity_name = entity_dict[self.ENTITY_NAME_TAG][0]
            entity_description = entity_dict[self.ENTITY_DESCRIPTION_TAG][0]
            entities.append(Artifact(id=entity_name, content=entity_description, layer_id=args.entity_layer_id, summary=""))
        state.entity_df = ArtifactDataFrame(entities)
