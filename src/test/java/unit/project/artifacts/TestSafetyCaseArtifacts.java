package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.repositories.artifacts.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;

import org.json.JSONArray;
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

    @Autowired
    ProjectRetrievalService projectRetrievalService;

    /**
     * Verifies that an SOLUTION node can be created.
     */
    @Test
    public void testCRUDSafetyNode() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        SafetyCaseType safetyCaseType = SafetyCaseType.SOLUTION;
        String safetyCaseTypeName = safetyCaseType.toString();
        String artifactBody = "this is a body";

        // Step - Create project with artifact type
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, safetyCaseTypeName)
            .newVersionWithReturn(projectName);

        // Step - Create payload for safety cases solution node
        JSONObject scArtifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withSafetyCaseArtifact(projectName, "", artifactName, safetyCaseTypeName, artifactBody, safetyCaseType)
            .getArtifact(projectName, artifactName);

        // Step - Send artifact creation request
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(scArtifactJson);
        JSONObject commitResponseJson = commit(commitBuilder);

        // VP - Verify that returned information is valid
        JSONArray artifactsAddedJson = commitResponseJson.getJSONObject("artifacts").getJSONArray("added");
        assertThat(artifactsAddedJson.length()).isEqualTo(1);
        JSONObject artifactAddedJson = artifactsAddedJson.getJSONObject(0);
        assertThat(artifactAddedJson.getString("name")).isEqualTo(artifactName);
        assertThat(artifactAddedJson.getString("id")).isNotEmpty();
        assertThat(artifactAddedJson.getString("documentType")).isEqualTo(DocumentType.SAFETY_CASE.toString());
        assertThat(artifactAddedJson.get("safetyCaseType")).isEqualTo(safetyCaseType.toString());

        // VP - Verify that safety case was created
        List<SafetyCaseArtifact> safetyCaseArtifacts =
            safetyCaseArtifactRepository.findByArtifactProject(projectVersion.getProject());
        assertThat(safetyCaseArtifacts.size()).isEqualTo(1);

        // VP - Verify that information is persisted
        SafetyCaseArtifact safetyCaseArtifact = safetyCaseArtifacts.get(0);
        assertThat(safetyCaseArtifact.getSafetyCaseType()).isEqualTo(safetyCaseType);
        assertThat(safetyCaseArtifact.getArtifact().getName()).isEqualTo(artifactName);

        // VP - Verify that retrieving project returns artifact
        List<ArtifactAppEntity> artifacts = projectRetrievalService.getArtifactsInProjectVersion(projectVersion);
        assertThat(artifacts.size()).isEqualTo(1);
        ArtifactAppEntity artifact = artifacts.get(0);
        assertThat(artifact.getDocumentType()).isEqualTo(DocumentType.SAFETY_CASE);
        assertThat(artifact.getSafetyCaseType()).isEqualTo(safetyCaseType);

        // Step - Delete artifact
        CommitBuilder deleteCommitBuilder =
            CommitBuilder.withVersion(projectVersion).withRemovedArtifact(artifactAddedJson);
        commit(deleteCommitBuilder);

        // Step - Recreate artifact
        CommitBuilder createCommitBuilder =
            CommitBuilder.withVersion(projectVersion).withAddedArtifact(artifactAddedJson);
        commit(createCommitBuilder);

        // VP - Verify that safety case was created
        safetyCaseArtifacts = safetyCaseArtifactRepository.findByArtifactProject(projectVersion.getProject());
        assertThat(safetyCaseArtifacts.size()).isEqualTo(1);

        // VP - Verify that information is persisted
        safetyCaseArtifact = safetyCaseArtifacts.get(0);
        assertThat(safetyCaseArtifact.getSafetyCaseType()).isEqualTo(safetyCaseType);
        assertThat(safetyCaseArtifact.getArtifact().getName()).isEqualTo(artifactName);
    }
}
