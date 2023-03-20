from data.datasets.data_key import DataKey
from models.llama.llama_model_manager import LLaMAModelManager
from models.llama.llama_task import LLaMATask
from testres.base_test import BaseTest
from util.object_creator import ObjectCreator


class TestLLaMAModelManager(BaseTest):

    def test_get_feature(self):

        def assert_features(feature, expected_length):
            self.assertIn(DataKey.INPUT_IDS, feature)
            self.assertIn(DataKey.ATTEN_MASK, feature)
            self.assertEquals(len(feature[DataKey.INPUT_IDS]), expected_length)
            self.assertEquals(len(feature[DataKey.INPUT_IDS]), expected_length)

        text = ["source_tokens1", "source_tokens2"]
        text_pair = ["target_tokens1", "target_tokens2"]
        cls_mm = self.get_model_manager()
        cls_feature = cls_mm.get_feature(text=text[0], text_pair=text_pair[0])
        assert_features(cls_feature, 1)

        sim_mm = self.get_model_manager(task=LLaMATask.SEQUENCE_SIMILARITY)
        sim_feature = sim_mm.get_feature(text=text, text_pair=text_pair)
        assert_features(sim_feature, 2)
        # because similarity is bi-directional
        self.assertEquals(len(sim_feature[DataKey.INPUT_IDS][0]), 2*len(cls_feature[DataKey.INPUT_IDS][0]))
        self.assertEquals(len(sim_feature[DataKey.ATTEN_MASK][0]), 2 * len(cls_feature[DataKey.ATTEN_MASK][0]))

    def get_model_manager(self, task=LLaMATask.SEQUENCE_CLASSIFICATION, ):
        model_manager_definition = ObjectCreator.get_definition(LLaMAModelManager)
        model_manager_definition.pop("object_type")
        model_manager_definition["model_task"] = task
        return LLaMAModelManager.initialize_from_definition(model_manager_definition)
