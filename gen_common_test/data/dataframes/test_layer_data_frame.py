from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.keys.structure_keys import LayerKeys
from gen_common.util import EnumDict
from gen_common_test.base_tests.base_test import BaseTest


class TestLayerDataFrame(BaseTest):

    def test_add_layer(self):
        df = self.get_layer_data_frame()
        layer = df.add_layer("source3", "target3")
        self.assert_layer(layer, "source3", "target3")

        df_empty = LayerDataFrame()
        layer = df_empty.add_layer("source3", "target3")
        self.assert_layer(layer, "source3", "target3")

    def assert_layer(self, layer: EnumDict, source_type, target_type):
        self.assertEqual(layer[LayerKeys.SOURCE_TYPE], source_type)
        self.assertEqual(layer[LayerKeys.TARGET_TYPE], target_type)

    def get_layer_data_frame(self):
        return LayerDataFrame({LayerKeys.SOURCE_TYPE: ["source1", "source2"], LayerKeys.TARGET_TYPE: ["target1", "target2"]})
