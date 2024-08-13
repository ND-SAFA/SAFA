import random

import mock
from sentence_transformers import CrossEncoder

from common_resources.tools.constants.hugging_face_constants import SMALL_CROSS_ENCODER
from tgen.relationship_manager.cross_encoder_manager import CrossEncoderManager
from tgen.testres.base_tests.base_test import BaseTest


class TestCrossEncoderManager(BaseTest):
    artifacts1 = ["Dogs are really cute.", "Car goes vroom."]
    artifacts2 = ["Fire trucks are loud.", "Dogs pee on fire hydrants."]

    def test_compare_artifacts_no_existing_relationships(self):
        ce_manager, ids1, ids2 = self.get_cross_encoder()
        sim_matrix = ce_manager.compare_artifacts(ids1, ids2)
        self.assertGreater(sim_matrix[0][1], sim_matrix[0][0])
        self.assertGreater(sim_matrix[1][0], sim_matrix[1][1])

    @mock.patch.object(CrossEncoder, "predict")
    def test_compare_artifacts_existing_relationships(self, predict_mock: mock.MagicMock = None):
        mocked_scores = [0.11, 0.22]
        predict_mock.return_value = mocked_scores
        ce_manager, ids1, ids2 = self.get_cross_encoder()
        for id1 in ids1:
            for id2 in ids2:
                ce_manager.add_relationship(id1, id2, random.randint(0, 10) / 10)
        new_id, new_artifact = "new_id", "Cats are cool"
        ce_manager.update_or_add_content(new_id, new_artifact)

        ids2.append(new_id)
        sim_matrix = ce_manager.compare_artifacts(ids1, ids2)
        for i, score in enumerate(mocked_scores):
            self.assertEqual(sim_matrix[i][2], score)

    def get_cross_encoder(self):
        ids1 = [f"A_{i}" for i, _ in enumerate(self.artifacts1)]
        ids2 = [f"B_{i}" for i, _ in enumerate(self.artifacts2)]
        content_map = {i: content for i, content in zip(ids1, self.artifacts1)}
        content_map.update({i: content for i, content in zip(ids2, self.artifacts2)})
        ce_manager = CrossEncoderManager(content_map, model_name=SMALL_CROSS_ENCODER)
        return ce_manager, ids1, ids2
