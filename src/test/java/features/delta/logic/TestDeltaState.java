package features.delta.logic;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import features.base.DefaultProjectConstants;
import features.delta.base.AbstractDeltaTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
class TestDeltaState extends AbstractDeltaTest {


    /**
     * Tests that the following modifications are detected to the delta calculations:
     * <p>
     * - Artifact was added, modified, and removed
     *
     * @throws Exception Throws error if http request fails.
     */
    @Test
    void testDeltaStateInDefaultProject() throws Exception {

        // VP - Verify that # of entities in before version
        List<ArtifactVersion> originalBodies = this.artifactVersionRepository.findByProjectVersion(beforeVersion);
        assertThat(originalBodies).hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that # of entities in after version coincides with # of changes.
        List<ArtifactVersion> changedBodies = this.artifactVersionRepository.findByProjectVersion(afterVersion);
        assertThat(changedBodies).hasSize(Constants.N_CHANGES);

        // Step - Calculate delta between versions
        JSONObject projectDelta = SafaRequest
            .withRoute(AppRoutes.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .getWithJsonObject();
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");

        // VP - Verify that artifact changes are detected
        verifyArtifactInDelta(artifactDelta, "modified", Constants.ARTIFACT_MODIFIED);
        verifyArtifactInDelta(artifactDelta, "added", Constants.ARTIFACT_ADDED);
        verifyArtifactInDelta(artifactDelta, "removed", Constants.ARTIFACT_REMOVED);

        ProjectAppEntity beforeAppEntity = retrievalTestService.getProjectAtVersion(beforeVersion);
        List<String> beforeArtifactNames = beforeAppEntity.getArtifactNames();

        // VP - Verify added artifact does not exist in before version.
        assertThat(beforeArtifactNames)
            .doesNotContain(Constants.ARTIFACT_ADDED)
            .contains(Constants.ARTIFACT_REMOVED)
            .hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // Step - Collect list of artifact names in the after version.
        ProjectAppEntity afterAppEntity = retrievalTestService.getProjectAtVersion(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream()
            .map(a -> a.name)
            .collect(Collectors.toList());

        // VP - Verify that removed artifact not included
        assertThat(afterArtifactNames)
            .doesNotContain("D7")
            .contains("D12");

        // VP - Verify that no extra artifacts where created.
        assertThat(afterAppEntity.getArtifacts()).hasSize(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that trace link changes are detected
        JSONObject traceDelta = projectDelta.getJSONObject("traces");
        verifyNumOfChangesInDelta(traceDelta, "added", Constants.N_TRACES_ADDED);
        verifyNumOfChangesInDelta(traceDelta, "removed", Constants.N_TRACES_REMOVED);
        verifyNumOfChangesInDelta(traceDelta, "modified", Constants.N_TRACES_MODIFIED);
    }
}
