package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.db.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;
import unit.TestConstants;

public class TestDeltaController extends EntityBaseTest {

    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);

        Project project = entityBuilder.getProject(projectName);
        ProjectVersion beforeVersion = entityBuilder.getProjectVersion(projectName, 0);
        ProjectVersion afterVersion = entityBuilder.getProjectVersion(projectName, 1);

        // Step - Upload files to before version
        String beforeRouteName = String.format("/projects/%s/%s/flat-files",
            project.getProjectId().toString(),
            beforeVersion.getVersionId().toString());
        MockMultipartHttpServletRequestBuilder beforeRequest = createMultiPartRequest(beforeRouteName,
            ProjectPaths.PATH_TO_BEFORE_FILES);
        sendRequest(beforeRequest, MockMvcResultMatchers.status().isCreated());

        // Step - Upload modified files to after version
        String afterRouteName = String.format("/projects/%s/%s/flat-files",
            project.getProjectId().toString(),
            afterVersion.getVersionId().toString());
        MockMultipartHttpServletRequestBuilder afterRequest = createMultiPartRequest(afterRouteName,
            ProjectPaths.PATH_TO_AFTER_FILES);
        sendRequest(afterRequest, MockMvcResultMatchers.status().isCreated());

        List<ArtifactBody> originalBodies = this.artifactBodyRepository.findByProjectVersion(beforeVersion);
        List<ArtifactBody> changedBodies = this.artifactBodyRepository.findByProjectVersion(afterVersion);

        assertThat(originalBodies.size()).isEqualTo(TestConstants.N_ARTIFACTS);
        assertThat(changedBodies.size()).isEqualTo(3);

        // Step - Calculate delta
        String deltaRouteName = String.format("/projects/delta/%s/%s",
            beforeVersion.getVersionId().toString(),
            afterVersion.getVersionId().toString());
        JSONObject response = sendGet(deltaRouteName, MockMvcResultMatchers.status().isOk()).getJSONObject("body");
        assertThat(response.getJSONObject("modified").has("F3")).isTrue();
        assertThat(response.getJSONObject("removed").has("D7")).isTrue();
        assertThat(response.getJSONObject("added").has("M1")).isTrue();
        assertThat(response.getJSONArray("missingArtifacts").length()).isEqualTo(1);

        ProjectAppEntity beforeAppEntity = this.projectService.createApplicationEntity(beforeVersion);
        // assertThat(beforeAppEntity.getArtifacts().size()).isEqualTo(TestConstants.N_ARTIFACTS);
        List<String> beforeArtifactNames = beforeAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(beforeArtifactNames.contains("M1")).isFalse();
        assertThat(beforeArtifactNames.contains("D7")).isTrue();
        assertThat(beforeArtifactNames.size()).isEqualTo(TestConstants.N_ARTIFACTS);
        ProjectAppEntity afterAppEntity = this.projectService.createApplicationEntity(afterVersion);
        List<String> afterArtifactNames = afterAppEntity
            .getArtifacts()
            .stream().map(a -> a.name)
            .collect(Collectors.toList());
        assertThat(afterArtifactNames.contains("M1")).isTrue();
        assertThat(afterArtifactNames.contains("D7")).isFalse();
        assertThat(afterAppEntity.getArtifacts().size()).isEqualTo(TestConstants.N_ARTIFACTS);
    }
}
