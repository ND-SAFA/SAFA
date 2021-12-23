package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
public class TestModificationDetected extends ApplicationBaseTest {

    /**
     * Tests that modifications to artifact bodies are detected in
     * delta calculations
     *
     * @throws Exception Throws error if http request fails.
     */
    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";

        // Step - Create before and after version
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // VP - Verify that number of changes is detected
        List<ArtifactVersion> originalBodies = this.artifactVersionRepository.findByProjectVersion(beforeVersion);
        List<ArtifactVersion> changedBodies = this.artifactVersionRepository.findByProjectVersion(afterVersion);
        assertThat(originalBodies.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        assertThat(changedBodies.size()).isEqualTo(3);

        // Step - Calculate delta
        String deltaRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.calculateProjectDelta)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .get();
        JSONObject projectDelta = sendGet(deltaRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject("body");
        JSONObject artifactDelta = projectDelta.getJSONObject("artifacts");
        JSONObject traceDelta = projectDelta.getJSONObject("traces");

        // VP - Verify that artifact changes are detected
        assertThat(artifactDelta.getJSONObject("modified").has(getId(projectName, "F3"))).isTrue();
        assertThat(artifactDelta.getJSONObject("removed").has(getId(projectName, "D7"))).isTrue();
        assertThat(artifactDelta.getJSONObject("added").has(getId(projectName, "D12"))).isTrue();

        ProjectAppEntity beforeAppEntity = this.projectRetrievalService.retrieveApplicationEntity(beforeVersion);
        List<String> beforeArtifactNames = beforeAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(beforeArtifactNames.contains("D12")).isFalse();
        assertThat(beforeArtifactNames.contains("D7")).isTrue();
        assertThat(beforeArtifactNames.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        ProjectAppEntity afterAppEntity = this.projectRetrievalService.retrieveApplicationEntity(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(afterArtifactNames.contains("D12")).isTrue();
        assertThat(afterArtifactNames.contains("D7")).isFalse();
        assertThat(afterAppEntity.getArtifacts().size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);

        // VP - Verify that trace link changes are detected
        int nTracesAdded = traceDelta.getJSONObject("added").keySet().toArray().length;
        int nTracesModified = traceDelta.getJSONObject("modified").keySet().toArray().length;
        int nTracesRemoved = traceDelta.getJSONObject("removed").keySet().toArray().length;

        assertThat(nTracesAdded).isEqualTo(1);
        assertThat(nTracesModified).isEqualTo(0);
        assertThat(nTracesRemoved).isEqualTo(0);
    }
}
