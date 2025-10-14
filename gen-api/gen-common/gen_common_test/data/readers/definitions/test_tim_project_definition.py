from copy import deepcopy
from unittest.mock import patch

from gen_common.constants.dataset_constants import NO_CHECK
from gen_common.data.keys.safa_keys import SafaKeys
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.definitions.tim_project_definition import TimProjectDefinition
from gen_common.util.json_util import JsonUtil
from gen_common_test.base.tests.base_test import BaseTest


class TestTimProjectDefinition(BaseTest):
    """
    Tests that TIM project is able to convert to structured project.
    """
    file_name = "file.csv"
    artifact_type = "reqs"
    trace_matrix_name = "source_type2target_type"
    source = "source_type"
    target = "target_type"
    original = {
        SafaKeys.ARTIFACTS: [{
            SafaKeys.TYPE: artifact_type,
            SafaKeys.FILE: file_name
        }],
        SafaKeys.TRACES: [
            {
                SafaKeys.FILE: file_name,
                SafaKeys.SOURCE_ID: source,
                SafaKeys.TARGET_ID: target
            }
        ]
    }
    expected = {
        StructuredKeys.ARTIFACTS: {
            artifact_type: {
                StructuredKeys.PATH: file_name,
                StructuredKeys.COLS: "csv-artifacts"
            }
        },
        StructuredKeys.TRACES: {
            trace_matrix_name: {
                StructuredKeys.PATH: file_name,

                StructuredKeys.COLS: "csv-traces",
                StructuredKeys.Trace.SOURCE.value: source,
                StructuredKeys.Trace.TARGET.value: target
            }
        },
        StructuredKeys.CONVERSIONS: {
            **TimProjectDefinition.get_flattened_conversions()
        },
        StructuredKeys.OVERRIDES: {
            "allowed_orphans": NO_CHECK
        }
    }

    @patch.object(JsonUtil, "read_json_file")
    def test_read_project_definition(self, read_json_file_mock):
        """
        Tests that both artifacts and trace matrices are converted to structured format.
        """
        read_json_file_mock.return_value = deepcopy(self.original)
        project_definition = TimProjectDefinition.read_project_definition("fake_path")
        expected_project_definition = self.expected
        self.assertDictEqual(expected_project_definition, project_definition)

    def test_create_artifact_definitions(self):
        """
        Tests that artifact definition converted to structure format.
        """

        original_def = deepcopy(self.original)
        expected_def = deepcopy(self.expected[StructuredKeys.ARTIFACTS])
        artifact_definitions = TimProjectDefinition._create_artifact_definitions(original_def)
        self.assertDictEqual(expected_def, artifact_definitions)

    def test_create_trace_definitions(self):
        """
        Tests that trace definition converted to structure format.
        """

        original_def = {self.trace_matrix_name: deepcopy(self.original[SafaKeys.TRACES][0])}
        expected_def = deepcopy(self.expected[StructuredKeys.TRACES][self.trace_matrix_name])
        trace_definitions = TimProjectDefinition._create_trace_definitions(deepcopy(self.original))
        t_definition = trace_definitions[self.trace_matrix_name]
        self.assertDictEqual(expected_def, t_definition)

    def test_get_flattened_conversions(self):
        """
        Tests that conversions get flattened to contain all conversions in single 1 layer dictionary.
        """
        flattened_conversions = TimProjectDefinition.get_flattened_conversions()
        for conversion in flattened_conversions.values():
            for value in conversion.values():
                self.assertTrue(isinstance(value, str))
        expected_keys = ["json-artifacts", "json-traces", "csv-artifacts", "csv-traces"]
        self.assertListEqual(expected_keys, list(flattened_conversions.keys()))

    def test_get_file_format(self):
        """
        Tests that supported format is retrieved correctly.
        """
        datum = [("data.json", "json"), ("data.csv", "csv")]
        for file_name, file_format in datum:
            self.assertEqual(file_format, TimProjectDefinition.get_file_format(file_name))

    def test_get_file_format_unknown_format(self):
        """
        Tests that unsupported formats throw error.
        """
        unsupported_file = "data.xml"
        with self.assertRaises(ValueError) as e:
            TimProjectDefinition.get_file_format(unsupported_file)
        error_message = " ".join(map(str, e.exception.args))
        self.assertIn(unsupported_file, error_message)
