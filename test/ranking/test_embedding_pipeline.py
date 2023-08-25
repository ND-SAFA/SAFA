from typing import Dict, List

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.ranking_args import RankingArgs


class TestEmbeddingPipeline(BaseTest):
    parent_ids = ["p1"]
    children_ids = ["c1", "c2", "c3"]
    artifact_map = {
        "p1": "Be able to customize my gameplay via a settings menu.",
        "c1": "Represents an abstract class for creating generic menus with selectable options.",
        "c2": "Represents a generic button used to trigger an action upon click",
        "c3": "Represents a slider that when clicked will turn to the opposite of the current state, either on or off."
    }

    def test_create_predictions(self):
        """
        Tests that embeddings are able to create trace entries using the similarity scores.
        """
        artifact_entries = self.create_artifacts_entries(self.parent_ids, "parent")
        artifact_entries.extend(self.create_artifacts_entries(self.children_ids, "children"))
        artifact_df = ArtifactDataFrame(artifact_entries)
        ranking_args = RankingArgs(run_name="children2parent",
                                   artifact_df=artifact_df,
                                   parent_ids=self.parent_ids,
                                   children_ids=self.children_ids)
        pipeline = EmbeddingRankingPipeline(ranking_args)
        trace_entries = pipeline.run()
        self.assertGreater(trace_entries[0]["score"], trace_entries[1]["score"])
        self.assertGreater(trace_entries[0]["score"], trace_entries[2]["score"])

    def create_artifacts_entries(self, artifact_ids: List[str], artifact_type: str) -> List[Dict]:
        """
        Creates entries for artifact data frame.
        :param artifact_ids: The artifact ids to create entries for.
        :param artifact_type: The artifact type.
        :return: Entries to artifact data frame.
        """
        entries = []
        for a_id in artifact_ids:
            entry = {
                ArtifactKeys.ID.value: a_id,
                ArtifactKeys.CONTENT.value: self.artifact_map[a_id],
                ArtifactKeys.LAYER_ID.value: artifact_type
            }
            entries.append(entry)
        return entries
