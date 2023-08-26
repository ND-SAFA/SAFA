from typing import Dict, List
from unittest import TestCase

from test.tracing.code_tracer.code_tracer_test_util import CodeTracerTestUtil
from tgen.common.constants.tracing.code_tracer_constants import PACKAGE_EXPLANATION, PACKAGE_TYPE
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.code_tracer import CodeTracer


class TestCodeTracerUtil(BaseTest):

    def test_add_package_nodes(self):
        """
        Verifies that artifacts and trace links are added for code files.
        """
        trace_dataset = CodeTracerTestUtil.get_trace_dataset()
        code_tracer = CodeTracer(trace_dataset)
        code_tracer.add_package_nodes()

        self.assertEqual(7, len(trace_dataset.artifact_df))
        self.assertEqual(6, len(trace_dataset.trace_df))

        TestCodeTracerUtil.assert_package_exists(self, trace_dataset, ["src", "abc", "def", "ghi"])
        TestCodeTracerUtil.check_links(self, trace_dataset, {
            "src": ["abc", "def", "ghi"],
            "abc": ["src/abc/some_class.h"],
            "def": ["src/def/some_class.cpp"],
            "ghi": ["src/ghi/some_class.cc"]
        })

    def test_extract_packages(self):
        """
        Verifies that packages are extracted in hierarchical order.
        """
        file_paths = [
            "src/data/data_module.py",
            "src/loader/data_loader.py"
        ]
        packages = CodeTracer.extract_packages(file_paths)
        self.assertEqual(3, len(packages))
        self.assertIn("src", packages)
        self.assertEqual(2, len(packages["src"]))
        self.assertIn("data", packages["src"])
        self.assertIn("loader", packages["src"])

        self.assertIn("data", packages)
        self.assertEqual(1, len(packages["data"]))
        self.assertIn("src/data/data_module.py", packages["data"])

        self.assertIn("loader", packages)
        self.assertEqual(1, len(packages["loader"]))
        self.assertIn("src/loader/data_loader.py", packages["loader"])

    @staticmethod
    def check_links(tc: TestCase, trace_dataset: TraceDataset, links: Dict[str, List[str]]):
        for parent, children in links.items():
            for c in children:
                link = trace_dataset.trace_df.get_link(source_id=c, target_id=parent)
                tc.assertIsNotNone(link, msg=f"No trace link between: {c} -> {parent}")
                tc.assertEqual(1, link[TraceKeys.LABEL])
                tc.assertEqual(PACKAGE_EXPLANATION, link[TraceKeys.EXPLANATION])

    @staticmethod
    def assert_package_exists(tc: TestCase, trace_dataset: TraceDataset, packages: List[str]):
        for p in packages:
            artifact = trace_dataset.artifact_df.get_artifact(p)
            tc.assertIsNotNone(artifact)
            tc.assertEqual(PACKAGE_TYPE, artifact[ArtifactKeys.LAYER_ID])
