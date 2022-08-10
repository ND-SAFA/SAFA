package features.delta.logic;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;

import features.delta.base.AbstractDeltaTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that the delta between two project versions can be calculated in the opposite direction
 * (e.g. from present version to past versions).
 */
class TestBackwardComparisons extends AbstractDeltaTest {

    @Test
    void backwardsVersioning() throws Exception {
        // Step - Calculate Delta in Backwards direction
        JSONObject projectDelta = new SafaRequest(AppRoutes.Projects.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(afterVersion)
            .withTargetVersion(beforeVersion)
            .getWithJsonObject();

        // VP - Verify that artifact changes are flipped
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");
        verifyArtifactInDelta(artifactDelta, "modified", Constants.ARTIFACT_MODIFIED);
        verifyArtifactInDelta(artifactDelta, "added", Constants.ARTIFACT_REMOVED);
        verifyArtifactInDelta(artifactDelta, "removed", Constants.ARTIFACT_ADDED);

        // VP -
        JSONObject traceDelta = projectDelta.getJSONObject("traces");
        verifyNumOfChangesInDelta(traceDelta, "added", Constants.N_TRACES_ADDED);
        verifyNumOfChangesInDelta(traceDelta, "modified", Constants.N_TRACES_MODIFIED);
        verifyNumOfChangesInDelta(traceDelta, "removed", Constants.N_TRACES_REMOVED);
    }
}
