import stanza

from tgen.common.constants.deliminator_constants import EMPTY_STRING, SPACE, F_SLASH
from tgen.common.objects.artifact import Artifact
from tgen.common.util.str_util import StrUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class IdentifyEntitiesStep(AbstractPipelineStep):
    """
    Attempts to find all entities used in the artifact content.
    """

    def __init__(self):
        """
        Initializes the pipeline from StandfordNLP.
        """
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Finds any entities that are mentioned in target artifact.
        :param args: Contains concepts and target artifact.
        :param state: Contains running list of matches.
        :return: None
        """
        if args.use_llm_for_entity_extraction:
            return

        direct_match_content = {match["matched_content"] for match in state.direct_matches}
        entity_data_frames = []
        for artifact in args.artifacts:
            target_artifact_content = artifact[ArtifactKeys.CONTENT]
            doc = self.nlp(target_artifact_content)
            entities = {self.process_entity(e.text) for e in doc.entities if e.text not in direct_match_content}
            artifacts = [Artifact(id=e, content=EMPTY_STRING, layer_id=args.entity_layer_id)
                         for e in entities if len(e) > 1 and not StrUtil.is_number(e)]
            entity_data_frames.append(ArtifactDataFrame(artifacts))
        state.entity_data_frames = entity_data_frames

    @staticmethod
    def process_entity(entity):
        processed_entity = entity.replace(F_SLASH, SPACE)
        processed_entity = StrUtil.remove_stop_words(processed_entity)
        processed_entity = StrUtil.remove_common_words(processed_entity)
        return processed_entity
