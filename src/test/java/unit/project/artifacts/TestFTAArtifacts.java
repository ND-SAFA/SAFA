package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.FTANodeType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.artifacts.FTAArtifactRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestFTAArtifacts extends ApplicationBaseTest {

    @Autowired
    FTAArtifactRepository ftaArtifactRepository;

    /**
     * Verifies that an artifact can be created and updated through ArtifactController.
     */
    @Test
    public void testCreateAndRetrieveFTAArtifact() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        FTANodeType ftaType = FTANodeType.AND;
        String safetyCaseTypeName = ftaType.toString();
        String artifactBody = "this is a body";

        // Step - Create project with artifact type
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, safetyCaseTypeName)
            .newVersionWithReturn(projectName);

        // Step - Create payload for safety cases solution node
        JSONObject scArtifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withFTAArtifact(projectName, "", artifactName, safetyCaseTypeName, artifactBody, ftaType)
            .getArtifact(projectName, artifactName);

        // Step - Send artifact creation request
        CommitBuilder commitBuilder = CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(scArtifactJson);
        JSONObject commitResponseJson = commit(commitBuilder);

        // VP - Verify that returned information is valid
        JSONArray addedArtifactsJson = commitResponseJson.getJSONObject("artifacts").getJSONArray("added");
        assertThat(addedArtifactsJson.length()).isEqualTo(1);
        JSONObject artifactAdded = addedArtifactsJson.getJSONObject(0);
        assertThat(artifactAdded.getString("name")).isEqualTo(artifactName);
        assertThat(artifactAdded.getString("id")).isNotEmpty();
        assertThat(artifactAdded.getString("documentType")).isEqualTo(DocumentType.FTA.toString());
        assertThat(artifactAdded.get("logicType")).isEqualTo(ftaType.toString());

        // VP - Verify that safety case was created
        List<FTAArtifact> safetyCaseArtifacts =
            ftaArtifactRepository.findByArtifactProject(projectVersion.getProject());
        assertThat(safetyCaseArtifacts.size()).isEqualTo(1);

        // VP - Verify that information is persisted
        FTAArtifact safetyCaseArtifact = safetyCaseArtifacts.get(0);
        assertThat(safetyCaseArtifact.getLogicType()).isEqualTo(ftaType);
        assertThat(safetyCaseArtifact.getArtifact().getName()).isEqualTo(artifactName);

        // VP - Verify that retrieving project returns artifact
        List<ArtifactAppEntity> artifacts = projectRetrievalService.getArtifactsInProjectVersion(projectVersion);
        assertThat(artifacts.size()).isEqualTo(1);
        ArtifactAppEntity artifact = artifacts.get(0);
        assertThat(artifact.getDocumentType()).isEqualTo(DocumentType.FTA);
        assertThat(artifact.getLogicType()).isEqualTo(ftaType);
    }
}
