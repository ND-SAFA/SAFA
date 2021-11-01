package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.DeltaService;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestArtifactController extends EntityBaseTest {

    @Autowired
    DeltaService deltaService;

    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        String modifiedSummary = "this is a new summary";

        // Step - Create project with single version
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Create Artifact JSON
        JSONObject artifact = jsonBuilder
            .withProject(projectName, projectName)
            .withArtifactAndReturn(projectName, artifactName, "requirements", "this is a body");

        // Step - Send request to create artifact via json
        String versionId = projectVersion.getVersionId().toString();
        String url = String.format("/projects/versions/%s/artifacts", versionId);
        sendPost(url, artifact, status().isCreated());

        // Step - Modify artifact
        artifact.put("summary", modifiedSummary);

        // VP - Submit modified artifact for saving
        sendPost(url, artifact, status().isCreated());

        // Step - Retrieve ArtifactBodies
        List<ArtifactBody> artifactBodies = artifactBodyRepository.getBodiesWithName(projectVersion.getProject(),
            artifactName);

        // VP - Only single artifact body exist and contains modification
        assertThat(artifactBodies.size()).isEqualTo(1);
        ArtifactBody body = artifactBodies.get(0);
        assertThat(body.getModificationType()).isEqualTo(ModificationType.ADDED);
        assertThat(body.getSummary()).isEqualTo(modifiedSummary);
    }

    @Test
    public void testArtifactExists() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        String artifactType = "requirement";
        String projectId = entityBuilder.newProjectWithReturn(projectName).getProjectId().toString();
        String url = String.format("/projects/%s/artifacts/validate/%s", projectId, artifactName);

        // VP - Verify that status is okay and artifact does not exist
        JSONObject response = sendGet(url, status().isOk());
        boolean artifactExists = response.getJSONObject("body").getBoolean("artifactExists");
        assertThat(artifactExists).isFalse();

        // Step - Create artifact
        entityBuilder
            .newType(projectName, artifactType)
            .newArtifact(projectName, artifactType, artifactName);

        // VP - Verify that status is okay and artifact does not exist
        response = sendGet(url, status().isOk());
        artifactExists = response.getJSONObject("body").getBoolean("artifactExists");
        assertThat(artifactExists).isTrue();
    }
}
