package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.app.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.repositories.artifacts.SafetyCaseArtifactRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestSafetyCaseArtifacts extends ApplicationBaseTest {

    @Autowired
    SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    /**
     * Verifies that an artifact can be created and updated through ArtifactController.
     */
    @Test
    public void testCreateNode() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        SafetyCaseType artifactType = SafetyCaseType.SOLUTION;
        String artifactTypeName = artifactType.toString();
        String artifactBody = "this is a body";

        // Step - Create project with artifact type
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, artifactTypeName)
            .newVersionWithReturn(projectName);

        // Step - Create payload for safety cases solution node
        JSONObject scArtifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withSafetyCaseArtifact(projectName, "", artifactName, artifactTypeName, artifactBody, artifactType)
            .getArtifact(projectName, artifactName);

        // Step - Send artifact creation request
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(scArtifactJson);
        commit(commitBuilder);

        // VP - Verify that safety case was created
        List<SafetyCaseArtifact> safetyCaseArtifacts =
            safetyCaseArtifactRepository.findByArtifactProject(projectVersion.getProject());
        assertThat(safetyCaseArtifacts.size()).isEqualTo(1);

        // VP - Verify that information is persisted
        SafetyCaseArtifact safetyCaseArtifact = safetyCaseArtifacts.get(0);
        assertThat(safetyCaseArtifact.getSafetyCaseType()).isEqualTo(artifactType);
        assertThat(safetyCaseArtifact.getArtifact().getName()).isEqualTo(artifactName);
    }
}
