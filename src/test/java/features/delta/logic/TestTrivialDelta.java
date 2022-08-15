package features.delta.logic;

import java.util.List;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.delta.base.AbstractDeltaTest;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that changes made in future version do not affect past ones.
 */
class TestTrivialDelta extends AbstractDeltaTest {

    @Test
    void testComparisonAgainstSameVersion() throws Exception {
        String projectName = "testThatTrivialArtifactNotCalculated";

        // Step - Create empty before and after versions
        Pair<ProjectVersion, ProjectVersion> versionPair = createDualVersions(projectName, false);
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
        JSONObject projectDelta = new SafaRequest(AppRoutes.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .getWithJsonObject();

        // VP - Verify that no changes are detected in artifacts
        for (String entityName : List.of("artifacts", "traces")) {
            JSONObject entityDelta = projectDelta.getJSONObject(entityName);
            verifyNumOfChangesInDelta(entityDelta, "added", 0);
            verifyNumOfChangesInDelta(entityDelta, "removed", 0);
            verifyNumOfChangesInDelta(entityDelta, "modified", 0);
        }
    }
}
