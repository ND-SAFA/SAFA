from tgen_test.hgen.hgen_test_utils import HGenTestConstants, get_test_hgen_args
from tgen.clustering.base.cluster import Cluster
from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.common.constants.ranking_constants import DEFAULT_TEST_EMBEDDING_MODEL
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.hgen.common.content_refiner import ContentRefiner
from tgen.hgen.common.duplicate_detector import DuplicateType
from tgen.hgen.hgen_state import HGenState
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.testres.base_tests.base_test import BaseTest


class TestContentRefiner(BaseTest):

    def test_merge_original_with_refined_generations(self):
        refiner = self.get_refiner()
        state = refiner.state
        new_user_story = "new user story"
        new_cluster_id = "4"
        orig_cluster2keep = "0"
        refined_cluster2generations = {new_cluster_id: [new_user_story]}
        refined_generation2sources = {new_user_story: set()}
        selected_sources = [s for sources in list(state.cluster2artifacts.values())[1:] for i, s in enumerate(sources) if i % 2 == 0]
        new_source_clusters = {new_cluster_id: [EnumDict({ArtifactKeys.ID: id_}) for id_ in selected_sources]}
        dups2remove = {us for i, us in enumerate(HGenTestConstants.user_stories) if i > int(orig_cluster2keep)}
        refiner._merge_original_with_refined_generations(refined_cluster2generations,
                                                         refined_generation2sources,
                                                         new_source_clusters, dups2remove)
        self.assertIn(new_cluster_id, refined_cluster2generations)
        self.assertIn(orig_cluster2keep, refined_cluster2generations)
        self.assertEqual(refined_cluster2generations[orig_cluster2keep], state.cluster2generations[orig_cluster2keep])
        self.assertIn(new_user_story, refined_generation2sources)
        self.assertIn(refined_cluster2generations[orig_cluster2keep][0], refined_generation2sources)
        self.assertIn(new_cluster_id, new_source_clusters)
        self.assertIn(orig_cluster2keep, new_source_clusters)
        self.assertSetEqual(set(state.cluster2artifacts[orig_cluster2keep]),
                            {a[ArtifactKeys.ID] for a in new_source_clusters[orig_cluster2keep]})
        for c_id in state.cluster2generations:
            if c_id == orig_cluster2keep:
                continue
            self.assertNotIn(c_id, refined_cluster2generations)
            self.assertNotIn(c_id, new_source_clusters)
            for generation in state.cluster2generations[c_id]:
                self.assertNotIn(generation, refined_generation2sources)

    def test_create_new_source_clusters(self):
        refiner = self.get_refiner()
        orig_cluster2keep = "0"
        duplicate_cluster_map = {"0": Cluster.from_artifact_map({str(i): us
                                                                 for i, us in enumerate(HGenTestConstants.user_stories)
                                                                 if i > int(orig_cluster2keep)},
                                                                model_name=SMALL_EMBEDDING_MODEL)}
        generated_artifacts_df = ArtifactDataFrame({ArtifactKeys.ID: [str(i) for i in range(len(HGenTestConstants.user_stories))],
                                                    ArtifactKeys.CONTENT: [us for us in HGenTestConstants.user_stories],
                                                    ArtifactKeys.LAYER_ID: ["source" for _ in HGenTestConstants.user_stories]})
        new_source_clusters, dups2remove = refiner._create_new_source_clusters(duplicate_cluster_map, generated_artifacts_df)
        self.assertSetEqual({us for i, us in enumerate(HGenTestConstants.user_stories) if i != int(orig_cluster2keep)}, dups2remove)
        possible_sources = [s for sources in list(refiner.state.cluster2artifacts.values())[1:] for s in sources]
        for sources in new_source_clusters.values():
            for s in sources:
                self.assertTrue(s[ArtifactKeys.ID] in possible_sources)

    def test_calculate_n_targets_for_duplicate_cluster(self):
        artifact_ids = {str(i) for i in range(4)}
        embeddings_manager = EmbeddingsManager({}, model_name=DEFAULT_TEST_EMBEDDING_MODEL)
        intra_cluster = Cluster(embeddings_manager, DuplicateType.INTRA_CLUSTER.name)
        intra_cluster.artifact_id_set = artifact_ids
        inter_cluster = Cluster(embeddings_manager, DuplicateType.INTER_CLUSTER.name)
        inter_cluster.artifact_id_set = artifact_ids

        self.assertEqual(ContentRefiner._calculate_n_targets_for_duplicate_cluster(intra_cluster), 1)
        self.assertEqual(ContentRefiner._calculate_n_targets_for_duplicate_cluster(inter_cluster), len(artifact_ids))

        originating_clusters = intra_cluster.get_originating_clusters()
        originating_clusters.extend([intra_cluster, inter_cluster])
        self.assertEqual(ContentRefiner._calculate_n_targets_for_duplicate_cluster(intra_cluster), 5)

    def get_refiner(self):
        hgen_args = get_test_hgen_args()()
        source_artifacts = list(hgen_args.dataset.artifact_df.index)
        state = HGenState(source_dataset=hgen_args.dataset,
                          embedding_manager=EmbeddingsManager(content_map=hgen_args.dataset.artifact_df.to_map(),
                                                              model_name=DEFAULT_TEST_EMBEDDING_MODEL),
                          cluster2generations={str(i): [us] for i, us in enumerate(HGenTestConstants.user_stories)},
                          generations2sources={us: set() for us in HGenTestConstants.user_stories},
                          cluster2artifacts={str(i): [source_artifacts[i * 3 + j] for j in range(3)]
                                             for i in range(len(HGenTestConstants.user_stories))})
        refiner = ContentRefiner(hgen_args, state, DuplicateType.ALL)
        return refiner
