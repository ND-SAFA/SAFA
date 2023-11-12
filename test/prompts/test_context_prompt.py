from copy import deepcopy
from unittest import mock
from unittest.mock import MagicMock

import numpy as np

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.common.util.enum_util import EnumDict
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestContextPrompt(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id1", ArtifactKeys.CONTENT: "content1"}),
                 EnumDict({ArtifactKeys.ID: "id2", ArtifactKeys.CONTENT: "content2"})]
    PROMPT = "This is a prompt"

    @mock.patch("sklearn.preprocessing._data.minmax_scale")
    def test_build_embedding_manager(self, minmax_scale_mock: MagicMock):
        minmax_scale_mock.return_value = np.asarray([0.4, 0.6])
        embedding_manager = EmbeddingsManager(content_map={a[ArtifactKeys.ID]: a[ArtifactKeys.CONTENT] for a in self.ARTIFACTS},
                                              model_name=SMALL_EMBEDDING_MODEL)
        context_prompt = self.get_context_prompt()
        prompt = context_prompt.build(artifact=EnumDict({ArtifactKeys.ID: "target", ArtifactKeys.CONTENT: "target content2"}),
                                      embedding_manager=embedding_manager, context_threshold=0.6)
        related_artifact = self.ARTIFACTS[1]
        self.assertIn(related_artifact[ArtifactKeys.ID], prompt)
        self.assertIn(related_artifact[ArtifactKeys.CONTENT], prompt)

    def test_build_ids_provided(self):
        context_prompt = self.get_context_prompt(id_to_context_artifacts={"target": deepcopy(self.ARTIFACTS)})
        prompt = context_prompt.build(artifact=EnumDict({ArtifactKeys.ID: "target", ArtifactKeys.CONTENT: ["target_content"]}),
                                      context_threshold=0.6)
        for related_artifact in self.ARTIFACTS:
            self.assertIn(related_artifact[ArtifactKeys.ID], prompt)
            self.assertIn(related_artifact[ArtifactKeys.CONTENT], prompt)

    def get_context_prompt(self, **params):
        return ContextPrompt(build_method=MultiArtifactPrompt.BuildMethod.XML, **params)
