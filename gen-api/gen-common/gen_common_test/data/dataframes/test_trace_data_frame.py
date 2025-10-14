from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.util.enum_util import EnumDict
from gen_common_test.base.tests.base_test import BaseTest


class TestTraceDataFrame(BaseTest):

    def test_add_link(self):
        df = self.get_trace_data_frame()
        link = df.add_link(source="s3", target="t3", label=1)
        self.assert_link(link, "s3", "t3", 1, TraceDataFrame.generate_link_id("s3", "t3"))

        df_empty = TraceDataFrame()
        link = df_empty.add_link(source="s3", target="t3", label=1)
        self.assert_link(link, "s3", "t3", 1, TraceDataFrame.generate_link_id("s3", "t3"))

    def test_get_link(self):
        df = self.get_trace_data_frame()
        link = df.get_link(source_id="s2", target_id="t2")
        self.assert_link(link, "s2", "t2", 1, TraceDataFrame.generate_link_id("s2", "t2"))

        link_does_not_exist = df.get_link(source_id="s3", target_id="t3")
        self.assertIsNone(link_does_not_exist)

    def test_to_dict(self):
        df = TraceDataFrame(EnumDict({TraceKeys.SOURCE: ["s1", "s1"], TraceKeys.TARGET: ["t1", "t1"],
                                      TraceKeys.LABEL: [0, 1]}))
        without_dups = df.to_dict(orient="index")
        self.assertSize(1, without_dups)

    def test_get_orphans(self):
        trace_dataset_frame = self.get_trace_data_frame()
        child_orphans = trace_dataset_frame.get_orphans(artifact_role=TraceKeys.child_label())
        self.assertSetEqual(child_orphans, {"s1"})
        parent_orphans = trace_dataset_frame.get_orphans(artifact_role=TraceKeys.parent_label())
        self.assertSetEqual(parent_orphans, {"t1"})

    def test_get_relationship(self):
        trace_dataset_frame = self.get_trace_data_frame()
        target_artifact = "s2"
        expected_children = ["child"]
        expected_parents = ["t2", "t3"]
        trace_dataset_frame.add_link(source=target_artifact, target="t1", label=0)
        trace_dataset_frame.add_link(source=target_artifact, target=expected_parents[-1], score=0.8)
        trace_dataset_frame.add_link(source=expected_children[0], target=target_artifact, score=0.8)

        parent_links = self._assert_relationships(target_artifact, trace_dataset_frame, expected_parents, TraceKeys.child_label())
        child_links = self._assert_relationships(target_artifact, trace_dataset_frame, expected_children, TraceKeys.parent_label())

        all_links = trace_dataset_frame.get_relationships(target_artifact)
        expected_links = parent_links + child_links
        self.assertSetEqual({trace[TraceKeys.LINK_ID] for trace in all_links}, {trace[TraceKeys.LINK_ID] for trace in expected_links})

    def _assert_relationships(self, target_artifact, trace_dataset_frame, expected_relations, target_key):
        relationships = trace_dataset_frame.get_relationships(target_artifact, artifact_key=target_key)
        relation_types = [TraceKeys.child_label(), TraceKeys.parent_label()]
        relation_key = relation_types[1 - relation_types.index(target_key)]
        self.assertEqual(len(relationships), len(expected_relations))
        for link in relationships:
            self.assertEqual(link[target_key], target_artifact)
            self.assertIn(link[relation_key], expected_relations)
        return relationships

    def assert_link(self, link: EnumDict, source_id, target_id, label, link_id):
        self.assertEqual(link[TraceKeys.SOURCE], source_id)
        self.assertEqual(link[TraceKeys.TARGET], target_id)
        self.assertEqual(link[TraceKeys.LABEL], label)
        self.assertEqual(link[TraceKeys.LINK_ID], link_id)

    def get_trace_data_frame(self):
        return TraceDataFrame(EnumDict({TraceKeys.SOURCE: ["s1", "s2"], TraceKeys.TARGET: ["t1", "t2"],
                                        TraceKeys.LABEL: [0, 1]}))
