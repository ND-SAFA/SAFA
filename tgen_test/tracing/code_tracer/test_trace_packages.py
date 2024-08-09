from typing import Dict, List
from unittest import TestCase

from tgen_test.tracing.code_tracer.code_tracer_test_util import CodeTracerTestUtil
from tgen.common.constants.code_tracer_constants import DEFAULT_PACKAGE_ARTIFACT_TYPE, PACKAGE_EXPLANATION
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys, LayerKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.tracing.code.code_tracer import CodeTracer
from tgen.tracing.code.package_tracer import PackageTracer


class TestPackageTracer(BaseTest):

    def test_add_package_nodes(self):
        """
        Verifies that artifacts and trace links are added for code files.
        """
        trace_dataset = CodeTracerTestUtil.get_trace_dataset()
        code_tracer = CodeTracer(trace_dataset)
        code_tracer.add_package_nodes()

        self.assertEqual(7, len(trace_dataset.artifact_df))
        self.assertEqual(6, len(trace_dataset.trace_df))
        self.assertEqual(2, len(trace_dataset.layer_df))

        TestPackageTracer.assert_package_exists(self, trace_dataset, ["src", "src/abc", "src/def", "src/ghi"])
        TestPackageTracer.check_links(self, trace_dataset, {
            "src": ["src/abc", "src/def", "src/ghi"],
            "src/abc": ["src/abc/some_class.h"],
            "src/def": ["src/def/some_class.cpp"],
            "src/ghi": ["src/ghi/some_class.cc"]
        })
        TestAssertions.verify_entities_in_df(self, [
            {LayerKeys.SOURCE_TYPE.value: DEFAULT_PACKAGE_ARTIFACT_TYPE, LayerKeys.TARGET_TYPE.value: DEFAULT_PACKAGE_ARTIFACT_TYPE},
            {LayerKeys.SOURCE_TYPE.value: CodeTracerTestUtil.code_artifact_type,
             LayerKeys.TARGET_TYPE.value: DEFAULT_PACKAGE_ARTIFACT_TYPE}
        ], trace_dataset.layer_df)

    def test_extract_packages(self):
        """
        Verifies that packages are extracted in hierarchical order.
        """
        file_paths = [
            "src/data/data_module.py",
            "src/loader/data_loader.py"
        ]
        package_hierarchy, package_set = PackageTracer._extract_package_hierarchy(file_paths)
        self.assertEqual(3, len(package_hierarchy))
        self.assertIn("src", package_hierarchy)
        self.assertEqual(2, len(package_hierarchy["src"]))
        self.assertIn("src/data", package_hierarchy["src"])
        self.assertIn("src/loader", package_hierarchy["src"])

        self.assertIn("src/data", package_hierarchy)
        self.assertEqual(1, len(package_hierarchy["src/data"]))
        self.assertIn("src/data/data_module.py", package_hierarchy["src/data"])

        self.assertIn("src/loader", package_hierarchy)
        self.assertEqual(1, len(package_hierarchy["src/loader"]))
        self.assertIn("src/loader/data_loader.py", package_hierarchy["src/loader"])

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
            tc.assertEqual(DEFAULT_PACKAGE_ARTIFACT_TYPE, artifact[ArtifactKeys.LAYER_ID])
