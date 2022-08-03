package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.DefaultProjectConstants;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
class TestDeltaState extends BaseDeltaTest {


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
        assertThat(originalBodies.size()).isEqualTo(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that # of entities in after version coincides with # of changes.
        List<ArtifactVersion> changedBodies = this.artifactVersionRepository.findByProjectVersion(afterVersion);
        assertThat(changedBodies.size()).isEqualTo(Constants.N_CHANGES);

        // Step - Calculate delta between versions
        JSONObject projectDelta = SafaRequest
            .withRoute(AppRoutes.Projects.Delta.CALCULATE_PROJECT_DELTA)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .getWithJsonObject();
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");

        // VP - Verify that artifact changes are detected
        verifyArtifactInDelta(artifactDelta, "modified", Constants.ARTIFACT_MODIFIED);
        verifyArtifactInDelta(artifactDelta, "added", Constants.ARTIFACT_ADDED);
        verifyArtifactInDelta(artifactDelta, "removed", Constants.ARTIFACT_REMOVED);

        ProjectAppEntity beforeAppEntity = getProjectAtVersion(beforeVersion);
        List<String> beforeArtifactNames = beforeAppEntity.getArtifactNames();

        // VP - Verify added artifact does not exist in before version.
        assertThat(beforeArtifactNames.contains(Constants.ARTIFACT_ADDED)).isFalse();
        assertThat(beforeArtifactNames.contains(Constants.ARTIFACT_REMOVED)).isTrue();

        // VP - Verify that no artifacts were added to before version.
        assertThat(beforeArtifactNames.size()).isEqualTo(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // Step - Collect list of artifact names in the after version.
        ProjectAppEntity afterAppEntity = getProjectAtVersion(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream()
            .map(a -> a.name)
            .collect(Collectors.toList());

        // VP - Verify that removed artifact not included
        assertThat(afterArtifactNames.contains("D7")).isFalse();

        // VP - Verify that artifact added in after version is retrieved.
        assertThat(afterArtifactNames.contains("D12")).isTrue();

        // VP - Verify that no extra artifacts where created.
        assertThat(afterAppEntity.getArtifacts().size()).isEqualTo(DefaultProjectConstants.Entities.N_ARTIFACTS);

        // VP - Verify that trace link changes are detected
        JSONObject traceDelta = projectDelta.getJSONObject("traces");
        verifyNumOfChangesInDelta(traceDelta, "added", Constants.N_TRACES_ADDED);
        verifyNumOfChangesInDelta(traceDelta, "removed", Constants.N_TRACES_REMOVED);
        verifyNumOfChangesInDelta(traceDelta, "modified", Constants.N_TRACES_MODIFIED);
    }
}
