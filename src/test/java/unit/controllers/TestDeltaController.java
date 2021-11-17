package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.DeltaService;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;
import unit.TestConstants;

public class TestDeltaController extends ApplicationBaseTest {

    @Autowired
    DeltaService deltaService;

    @Autowired
    ProjectRetrievalService projectRetrievalService;

    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";

        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // VP - Verify that number of changes is detected
        List<ArtifactBody> originalBodies = this.artifactBodyRepository.findByProjectVersion(beforeVersion);
        List<ArtifactBody> changedBodies = this.artifactBodyRepository.findByProjectVersion(afterVersion);

        assertThat(originalBodies.size()).isEqualTo(TestConstants.N_ARTIFACTS);
        assertThat(changedBodies.size()).isEqualTo(3);

        // Step - Calculate delta
        String deltaRouteName = String.format("/projects/delta/%s/%s",
            beforeVersion.getVersionId().toString(),
            afterVersion.getVersionId().toString());
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
        assertThat(beforeArtifactNames.size()).isEqualTo(TestConstants.N_ARTIFACTS);
        ProjectAppEntity afterAppEntity = this.projectRetrievalService.createApplicationEntity(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(afterArtifactNames.contains("M1")).isTrue();
        assertThat(afterArtifactNames.contains("D7")).isFalse();
        assertThat(afterAppEntity.getArtifacts().size()).isEqualTo(TestConstants.N_ARTIFACTS);
    }

    @Test
    public void backwardsVersioning() throws Exception {
        String projectName = "backward-versioning";
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Calculate Delta in Backwards direction
        String backwardRouteName = String.format("/projects/delta/%s/%s",
            afterVersion.getVersionId().toString(),
            beforeVersion.getVersionId().toString());
        JSONObject backwardResponse = sendGet(backwardRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject(
            "body");
        assertThat(backwardResponse.getJSONObject("modified").has("F3")).isTrue();
        assertThat(backwardResponse.getJSONObject("removed").has("M1")).isTrue();
        assertThat(backwardResponse.getJSONObject("added").has("D7")).isTrue();
    }

    @Test
    public void testThatTrivialArtifactNotCalculated() throws Exception {
        String projectName = "backward-versioning";

        // Step - Create empty before and after versions
        Pair<ProjectVersion, ProjectVersion> versionPair = setupDualVersions(projectName, false);
        ProjectVersion beforeVersion = versionPair.getValue0();
        ProjectVersion afterVersion = versionPair.getValue1();

        // Step - Create future version with single change (artifact addition)
        ProjectVersion trivialVersion = entityBuilder.newVersionWithReturn(projectName);
        String dummySummary = "this is a summary";
        String dummyContent = "this is a content";
        entityBuilder
            .newType(projectName, "requirement")
            .newArtifact(projectName, "requirement", "RE-NA");
        entityBuilder.newArtifactBody(projectName, 2, "RE-NA", dummySummary, dummyContent);

        // Step - Send Delta Request
        String backwardRouteName = String.format("/projects/delta/%s/%s",
            beforeVersion.getVersionId().toString(),
            afterVersion.getVersionId().toString());
        JSONObject response = sendGet(backwardRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject(
            "body");
        assertThat(response.getJSONObject("added").keySet().size()).isEqualTo(0);
        assertThat(response.getJSONObject("removed").keySet().size()).isEqualTo(0);
        assertThat(response.getJSONObject("modified").keySet().size()).isEqualTo(0);
    }

    private Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName) throws Exception {
        return setupDualVersions(projectName, true);
    }

    private Pair<ProjectVersion, ProjectVersion> setupDualVersions(String projectName, boolean uploadFiles) throws Exception {
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        ProjectVersion beforeVersion = entityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = entityBuilder.getProjectVersion(projectName, 1);

        if (uploadFiles) {
            uploadFlatFilesToVersion(beforeVersion, ProjectPaths.PATH_TO_BEFORE_FILES);
            uploadFlatFilesToVersion(afterVersion, ProjectPaths.PATH_TO_AFTER_FILES);
        }

        return new Pair<>(beforeVersion, afterVersion);
    }
}
