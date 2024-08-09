from tgen_test.jobs.health_check_jobs.health_check_constants import QUERY
from tgen_test.jobs.health_check_jobs.health_check_utils import assert_correct_related_artifacts, assert_correct_related_traces, \
    get_dataset_for_context
from tgen.common.constants.hugging_face_constants import SMALL_CROSS_ENCODER, SMALL_EMBEDDING_MODEL
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.context_finder import ContextFinder


class TestContextFinder(BaseTest):

    def test_find_related_artifacts(self):
        dataset = get_dataset_for_context(include_query=True)
        query_id = QUERY[ArtifactKeys.ID]
        id2context, all_relationships = ContextFinder.find_related_artifacts(query_id, dataset,
                                                                             ranking_model_name=SMALL_CROSS_ENCODER,
                                                                             embedding_model_name=SMALL_EMBEDDING_MODEL)
        assert_correct_related_artifacts(self, [a[ArtifactKeys.ID] for a in id2context[query_id]])
        assert_correct_related_traces(self, all_relationships)
