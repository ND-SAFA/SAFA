package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
public class TestDeletedTraceLink extends ApplicationBaseTest {

    /**
     * Tests that modifications to artifact bodies are detected in
     * delta calculations
     *
     * @throws Exception Throws error if http request fails.
     */
    @Test
    public void test() throws Exception {
        String projectName = "test-project";
        String artifactOneName = "RE-10";
        String artifactTwoName = "F-20";
        String artifactType = "requirement";
        String artifactBody = "this is a body";

        // Step - Create before and after version
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName, false);
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
        ArtifactAppEntity secondArtifact =
            projectCommit.getArtifacts().filterAdded(a -> a.name.equals(artifactTwoName));

        // Step - Commit deleted artifactOne
        JSONObject commitJson = commit(CommitBuilder
            .withVersion(afterVersion)
            .withRemovedArtifact(toJson(firstArtifact)));
        ProjectCommit commit = toClass(commitJson.toString(), ProjectCommit.class);

        // DEBUGGING
        String traceId = commit.getTraces().getRemoved().get(0).traceLinkId;
        List<TraceLinkVersion> afterLinks =
            traceLinkVersionRepository.findByTraceLinkTraceLinkId(UUID.fromString(traceId));

        for (TraceLinkVersion t : afterLinks) {
            System.out.println("Link version:" + t);
        }

        // Step - Calculate delta
        String deltaRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.Delta.calculateProjectDelta)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .get();
        JSONObject projectDelta = sendGet(deltaRouteName, MockMvcResultMatchers.status().isOk());
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");
        JSONObject traceDelta = projectDelta.getJSONObject("traces");

        // VP - Verify artifact was deleted
        int nArtifactsDeleted = artifactDelta.getJSONObject("removed").length();
        assertThat(nArtifactsDeleted).isEqualTo(1);

        // VP - Verify trace was deleted
        int nTracesDeleted = traceDelta.getJSONObject("removed").length();
        assertThat(nTracesDeleted).isEqualTo(1);
    }
}
