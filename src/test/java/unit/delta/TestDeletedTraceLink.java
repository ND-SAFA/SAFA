package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

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
        Pair<ProjectVersion, ProjectVersion> versionPair = createDualVersions(projectName, false);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Upload before version
        jsonBuilder.withProject(projectName, projectName, "");
        JSONObject artifactOne = jsonBuilder
            .withArtifactAndReturn(projectName, "", artifactOneName, artifactType, artifactBody);
        JSONObject artifactTwo = jsonBuilder
            .withArtifactAndReturn(projectName, "", artifactTwoName, artifactType, artifactBody);
        JSONObject traceJson = jsonBuilder
            .withTraceAndReturn(projectName, artifactOneName, artifactTwoName);

        // Step - Find artifact to delete
        JSONObject projectCommitJson = commit(CommitBuilder.withVersion(beforeVersion)
            .withAddedArtifact(artifactOne)
            .withAddedArtifact(artifactTwo)
            .withAddedTrace(traceJson));
        ProjectCommit projectCommit = toClass(projectCommitJson.toString(), ProjectCommit.class);
        ArtifactAppEntity firstArtifact = projectCommit.getArtifacts().filterAdded(a -> a.name.equals(artifactOneName));
        ArtifactAppEntity secondArtifact = // TODO: Remove or add test cases
            projectCommit.getArtifacts().filterAdded(a -> a.name.equals(artifactTwoName));

        // Step - Commit deleted artifactOne
        JSONObject commitJson = commit(CommitBuilder
            .withVersion(afterVersion)
            .withRemovedArtifact(JsonFileUtilities.toJson(firstArtifact)));
        ProjectCommit commit = toClass(commitJson.toString(), ProjectCommit.class);

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
            .withRoute(AppRoutes.Projects.Delta.calculateProjectDelta)
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
