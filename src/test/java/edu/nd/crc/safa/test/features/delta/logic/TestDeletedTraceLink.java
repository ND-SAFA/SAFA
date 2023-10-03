package edu.nd.crc.safa.test.features.delta.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
class TestDeletedTraceLink extends ApplicationBaseTest {

    String projectName = "test-project";
    String artifactOneName = "RE-10";
    String artifactTwoName = "F-20";
    String artifactType = "requirement";
    String artifactBody = "this is a body";

    /**
     * Tests that modifications to artifact bodies are detected in
     * delta calculations
     *
     * @throws Exception Throws error if http request fails.
     */
    @Test
    void test() throws Exception {
        // Step - Create before and after version
        Pair<ProjectVersion, ProjectVersion> versionPair = creationService
            .createDualVersions(projectName, false);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Upload before version
        jsonBuilder.withProject(projectName, projectName, "");
        JSONObject artifactOne = jsonBuilder
            .withArtifactAndReturn(projectName, null, artifactOneName, artifactType, artifactBody);
        JSONObject artifactTwo = jsonBuilder
            .withArtifactAndReturn(projectName, null, artifactTwoName, artifactType, artifactBody);
        JSONObject traceJson = jsonBuilder
            .withTraceAndReturn(projectName, artifactOneName, artifactTwoName);

        // Step - Find artifact to delete
        ProjectCommitDefinition addCommit = commitService.commit(CommitBuilder.withVersion(beforeVersion)
            .withAddedArtifact(artifactOne)
            .withAddedArtifact(artifactTwo)
            .withAddedTrace(traceJson));
        ArtifactAppEntity firstArtifact =
            addCommit.getArtifacts().filterAdded(a -> a.getName().equals(artifactOneName));

        // Step - Commit deleted artifactOne
        commitService.commit(CommitBuilder
            .withVersion(afterVersion)
            .withRemovedArtifact(JsonFileUtilities.toJson(firstArtifact)));

        // Step - Calculate delta
        verifyDelta(beforeVersion, afterVersion, "removed");

        // Step - Reverse delta
        verifyDelta(afterVersion, beforeVersion, "added");
    }

    private void verifyDelta(ProjectVersion beforeVersion,
                             ProjectVersion afterVersion,
                             String expectedChange) throws Exception {
        // Step - Reverse delta
        JSONObject projectDelta = SafaRequest
            .withRoute(AppRoutes.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .getWithJsonObject();

        // Step - Retrieve delta information
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");
        JSONObject traceDelta = projectDelta.getJSONObject("traces");

        // VP - Verify artifact was deleted
        int nChangedArtifacts = artifactDelta.getJSONObject(expectedChange).length();
        assertThat(nChangedArtifacts).isEqualTo(1);

        // VP - Verify trace was deleted
        int nChangedTraces = traceDelta.getJSONObject(expectedChange).length();
        assertThat(nChangedTraces).isEqualTo(1);
    }
}
