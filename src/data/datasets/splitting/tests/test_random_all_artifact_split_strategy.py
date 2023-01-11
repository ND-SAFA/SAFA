from typing import List

from data.datasets.splitting.random_all_artifact_split_strategy import RandomAllArtifactSplitStrategy
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink
from testres.base_test import BaseTest


class TestRandomAllArtifactSplitStrategy(BaseTest):
    """
    Test that different splits reference all artifacts and that error is thrown
    when unable to do so.
    """
    SOURCE_PREFIX = "S"
    TARGET_PREFIX = "T"
    N_SOURCES = 4
    N_TARGETS = 4
    N_LINKS = N_SOURCES * N_TARGETS
    SOURCES = [f"S{i}" for i in range(N_SOURCES)]
    TARGETS = [f"T{i}" for i in range(N_TARGETS)]
    EXPECTED_IDS = SOURCES + TARGETS

    def test_all_artifacts_present(self) -> None:
        """
        Tests that split contains reference to all artifacts.
        """
        validation_percentage = 0.5
        trace_dataset = self.create_trace_dataset()
        split = RandomAllArtifactSplitStrategy.create_split(trace_dataset, validation_percentage, 1)
        self.assert_split_correct(split, validation_percentage)

    def test_error_on_small_split(self):
        """
        Tests that if splitting leads to too many links, error is thrown.
        """
        validation_percentage = 0.25
        trace_dataset = self.create_trace_dataset()
        with self.assertRaises(ValueError) as e:
            RandomAllArtifactSplitStrategy.create_split(trace_dataset, validation_percentage, 1)
        self.assertIn(f"{validation_percentage}", e.exception.args[0])

    def assert_split_correct(self, split: TraceDataset, validation_percentage: float):
        split_links = list(split.links.values())
        self.assertEqual(len(split_links), self.N_LINKS * validation_percentage)
        self.assert_artifact_referenced(split_links, self.EXPECTED_IDS)

    def assert_artifact_referenced(self, links: List[TraceLink], expected_ids: List[str]) -> None:
        """
        Asserts that expected artifact ids are referenced in at least one link.
        :param links: The links containing references to artifacts.
        :param expected_ids: The artifact ids expected to be referenced
        :return: None
        """
        artifact_ids = []
        for link in links:
            if link.source.id not in artifact_ids:
                artifact_ids.append(link.source.id)
            if link.target.id not in artifact_ids:
                artifact_ids.append(link.target.id)

        for expected_id in expected_ids:
            self.assertIn(expected_id, artifact_ids)

    def create_trace_dataset(self) -> TraceDataset:
        links = {t.id: t for t in self.create_trace_links((self.SOURCE_PREFIX, self.TARGET_PREFIX),
                                                          (self.N_SOURCES, self.N_TARGETS),
                                                          [0] * self.N_LINKS)}
        return TraceDataset(links)
