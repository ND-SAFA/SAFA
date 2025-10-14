package edu.nd.crc.safa.test.features.delta.logic;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.test.features.delta.base.AbstractDeltaTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

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
        JSONObject projectDelta = new SafaRequest(AppRoutes.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(afterVersion)
            .withTargetVersion(beforeVersion)
            .getWithJsonObject();

        // VP - Verify that artifact changes are flipped
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");
        assertionService.verifyArtifactInDelta(retrievalService, projectName, artifactDelta, "modified",
            Constants.ARTIFACT_MODIFIED);
        assertionService.verifyArtifactInDelta(retrievalService, projectName, artifactDelta, "added",
            Constants.ARTIFACT_REMOVED);
        assertionService.verifyArtifactInDelta(retrievalService, projectName, artifactDelta, "removed",
            Constants.ARTIFACT_ADDED);

        // VP -
        JSONObject traceDelta = projectDelta.getJSONObject("traces");
        assertionService.verifyNumOfChangesInDelta(traceDelta, "added", Constants.N_TRACES_ADDED);
        assertionService.verifyNumOfChangesInDelta(traceDelta, "modified", Constants.N_TRACES_MODIFIED);
        assertionService.verifyNumOfChangesInDelta(traceDelta, "removed", Constants.N_TRACES_REMOVED);
    }
}
