package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Tests that the delta between two project versions can be calculated in the opposite direction
 * (e.g. from present version to past versions).
 */
public class TestBackwardComparisons extends ApplicationBaseTest {

    @Test
    public void backwardsVersioning() throws Exception {
        String projectName = "backward-versioning";
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Calculate Delta in Backwards direction
        String backwardRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.calculateProjectDelta)
            .withBaselineVersion(afterVersion)
            .withTargetVersion(beforeVersion)
            .get();
        JSONObject backwardResponse = sendGet(backwardRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject(
            "body");
        assertThat(backwardResponse.getJSONObject("modified").has("F3")).isTrue();
        assertThat(backwardResponse.getJSONObject("removed").has("M1")).isTrue();
        assertThat(backwardResponse.getJSONObject("added").has("D7")).isTrue();
    }

    @Test
    public void testComparisonAgainstSameVersion() throws Exception {
        String projectName = "testThatTrivialArtifactNotCalculated";

        // Step - Create empty before and after versions
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName, false);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Create future version with single change (artifact addition)
        dbEntityBuilder.newVersionWithReturn(projectName);
        String dummySummary = "this is a summary";
        String dummyContent = "this is a content";
        dbEntityBuilder
            .newType(projectName, "requirement")
            .newArtifact(projectName, "requirement", "RE-NA");
        dbEntityBuilder.newArtifactBody(projectName, 2, "RE-NA", dummySummary, dummyContent);

        // Step - Send Delta Request
        String backwardRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.calculateProjectDelta)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .get();
        JSONObject response = sendGet(backwardRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject(
            "body");
        //
        assertThat(response.getJSONObject("added").keySet().size()).isEqualTo(0);
        assertThat(response.getJSONObject("removed").keySet().size()).isEqualTo(0);
        assertThat(response.getJSONObject("modified").keySet().size()).isEqualTo(0);
    }
}
