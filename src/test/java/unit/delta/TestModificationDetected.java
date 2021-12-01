package unit.delta;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.SampleProjectConstants;

/**
 * Tests that changes to the content of artifacts are retrieved.
 */
public class TestModificationDetected extends DeltaBaseTest {

    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";

        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // VP - Verify that number of changes is detected
        List<ArtifactBody> originalBodies = this.artifactBodyRepository.findByProjectVersion(beforeVersion);
        List<ArtifactBody> changedBodies = this.artifactBodyRepository.findByProjectVersion(afterVersion);

        assertThat(originalBodies.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        assertThat(changedBodies.size()).isEqualTo(3);

        // Step - Calculate delta
        String deltaRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.calculateProjectDelta)
            .withBaselineVersion(beforeVersion)
            .withTargetVersion(afterVersion)
            .get();
        JSONObject response = sendGet(deltaRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject("body");

        // VP - Verify that changes are detected
        assertThat(response.getJSONObject("modified").has("F3")).isTrue();
        assertThat(response.getJSONObject("removed").has("D7")).isTrue();
        assertThat(response.getJSONObject("added").has("M1")).isTrue();
        assertThat(response.getJSONArray("missingArtifacts").length()).isEqualTo(1);

        ProjectAppEntity beforeAppEntity = this.projectRetrievalService.createApplicationEntity(beforeVersion);
        // assertThat(beforeAppEntity.getArtifacts().size()).isEqualTo(TestConstants.N_ARTIFACTS);
        List<String> beforeArtifactNames = beforeAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(beforeArtifactNames.contains("M1")).isFalse();
        assertThat(beforeArtifactNames.contains("D7")).isTrue();
        assertThat(beforeArtifactNames.size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
        ProjectAppEntity afterAppEntity = this.projectRetrievalService.createApplicationEntity(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(afterArtifactNames.contains("M1")).isTrue();
        assertThat(afterArtifactNames.contains("D7")).isFalse();
        assertThat(afterAppEntity.getArtifacts().size()).isEqualTo(SampleProjectConstants.N_ARTIFACTS);
    }
}
