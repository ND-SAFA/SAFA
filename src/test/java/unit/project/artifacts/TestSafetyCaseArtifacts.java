package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.repositories.artifacts.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestSafetyCaseArtifacts extends ApplicationBaseTest {

    @Autowired
    SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    @Autowired
    AppEntityRetrievalService appEntityRetrievalService;

    /**
     * Verifies that an SOLUTION node can be:
     * - created
     * - modified
     * - removed
     * - recreated
     * - delta calculation
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
        List<ArtifactAppEntity> artifacts = appEntityRetrievalService.retrieveArtifactsInProjectVersion(projectVersion);
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
        JSONObject recreatedCommit = commit(createCommitBuilder);
        String artifactId =
            recreatedCommit
                .getJSONObject("artifacts")
                .getJSONArray("added")
                .getJSONObject(0)
                .getString("id");

        // VP - Verify that safety case was created
        safetyCaseArtifacts = safetyCaseArtifactRepository.findByArtifactProject(projectVersion.getProject());
        assertThat(safetyCaseArtifacts.size()).isEqualTo(1);

        // VP - Verify that information is persisted
        safetyCaseArtifact = safetyCaseArtifacts.get(0);
        assertThat(safetyCaseArtifact.getSafetyCaseType()).isEqualTo(safetyCaseType);
        assertThat(safetyCaseArtifact.getArtifact().getName()).isEqualTo(artifactName);

        // Step - Modify artifact
        ProjectVersion newProjectVersion = this.dbEntityBuilder.newVersionWithReturn(projectName);
        String newArtifactBody = "new artifact body.";
        artifactAddedJson.put("body", newArtifactBody);

        // Step - Commit modified artifact
        commit(CommitBuilder
            .withVersion(newProjectVersion)
            .withModifiedArtifact(artifactAddedJson));

        // Step - Get project delta
        String deltaRouteName = RouteBuilder
            .withRoute(AppRoutes.Projects.Delta.calculateProjectDelta)
            .withBaselineVersion(projectVersion)
            .withTargetVersion(newProjectVersion)
            .get();
        JSONObject projectDelta = sendGet(deltaRouteName, MockMvcResultMatchers.status().isOk());

        // VP - Verify that change is detected
        JSONObject modifiedArtifacts = projectDelta.getJSONObject("artifacts").getJSONObject("modified");
        JSONObject modifiedArtifact = modifiedArtifacts.getJSONObject(artifactId);
        assertThat(modifiedArtifact.getJSONObject("before").getString("body")).isEqualTo(artifactBody);
        assertThat(modifiedArtifact.getJSONObject("after").getString("body")).isEqualTo(newArtifactBody);
    }
}
