import os

import pandas as pd

from tgen.data.github.gartifacts.gartifact_set import GArtifactSet
from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.github_test_project import GithubTestProject


class TestGArtifactSet(BaseTest):
    """
    Tests ability to load and save artifact sets.
    """

    def test_save(self):
        """
        Tests that saved artifacts can be reloaded.
        """
        issues = GArtifactSet.load(GithubTestProject.get_path(GArtifactType.ISSUE))
        export_path = os.path.join(TEST_OUTPUT_DIR, "test.csv")
        issues.export(export_path)
        data_df = pd.read_csv(export_path)
        self.assertEqual(len(issues), len(data_df))

    def test_filter(self):
        """
        Tests that filtering removes artifacts not referenced in filter list.
        """
        issues = GArtifactSet.load(GithubTestProject.get_path(GArtifactType.ISSUE))
        new_issues = issues.filter(["1"])
        self.assertEqual(2, len(issues))
        self.assertEqual(1, len(new_issues))

    def test_load(self):
        """
        Tests that reading test project contains all artifacts.
        """
        expected_ids = [GithubTestProject.get_issue_ids(), GithubTestProject.get_pull_ids(), GithubTestProject.get_commit_ids()]
        expected_artifacts = [2, 1, 1]
        artifact_files = [GithubTestProject.get_path(at) for at in [GArtifactType.ISSUE, GArtifactType.PULL, GArtifactType.COMMIT]]
        for artifact_ids, n_artifacts, artifact_file in zip(expected_ids, expected_artifacts, artifact_files):
            artifact_set = GArtifactSet.load(artifact_file)
            self.assertEqual(n_artifacts, len(artifact_set))
            for artifact_id in artifact_ids:
                self.assertIn(artifact_id, artifact_set)
