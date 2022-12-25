from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from test.base_test import BaseTest


class BaseTraceTest(BaseTest):

    def get_link_ids(self, links_list):
        return list(self.get_links(links_list).keys())

    @staticmethod
    def get_links(link_list):
        links = {}
        for source, target in link_list:
            link = BaseTraceTest.get_test_link(source, target)
            links[link.id] = link
        return links

    @staticmethod
    def get_test_link(source, target):
        s = Artifact(source, BaseTraceTest.ALL_TEST_SOURCES[source])
        t = Artifact(target, BaseTraceTest.ALL_TEST_TARGETS[target])
        return TraceLink(s, t)

    @staticmethod
    def get_test_artifacts(artifacts_dict):
        return [Artifact(id_, token) for id_, token in artifacts_dict.items()]
