package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.DeltaService;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is allowed to:
 * 1. Add new artifacts
 * 2. Modify existing artifacts
 * 3. Delete existing artifacts
 */
public class TestArtifactController extends ApplicationBaseTest {

    @Autowired
    DeltaService deltaService;

    /**
     * Verifies that an artifact can be created and updated through ArtifactController.
     */
    @Test
    public void testModificationDetected() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        String modifiedSummary = "this is a new summary";
        String modifiedName = "RE-42";

        // Step - Create a new artifact
        Pair<ProjectVersion, JSONObject> response = createArtifact(projectName, artifactName);
        ProjectVersion projectVersion = response.getValue0();
        Project project = projectVersion.getProject();
        JSONObject artifactJson = response.getValue1();

        // VP - Verify artifact exists
        int numberOfArtifacts = this.artifactRepository.findByProject(project).size();
        assertArtifactExists(projectVersion, artifactName);
        assertThat(numberOfArtifacts).isEqualTo(1);

        // Step - Modify artifact summary
        artifactJson.put("name", modifiedName);
        artifactJson.put("summary", modifiedSummary);

        // VP - Commit modified artifact for saving
        commit(CommitBuilder
            .withVersion(projectVersion)
            .withModifiedArtifact(artifactJson));

        // Step - Retrieve ArtifactBodies
        List<ArtifactVersion> artifactBodies = artifactVersionRepository.getEntitiesInProject(project);

        // VP - Verify one single artifact body
        List<Artifact> artifactInProject = this.artifactRepository.findByProject(project);
        numberOfArtifacts = artifactInProject.size();
        assertThat(numberOfArtifacts).isEqualTo(1);
        assertThat(artifactBodies.size()).isEqualTo(1);

        // VP - Verify body contains modification
        ArtifactVersion body = artifactBodies.get(0);
        assertThat(body.getModificationType()).isEqualTo(ModificationType.ADDED);
        assertThat(body.getSummary()).isEqualTo(modifiedSummary);
    }

    /**
     * Verifies that an artifact can be created and updated through ArtifactController.
     */
    @Test
    public void testDeleteArtifact() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";

        // Step - Create artifact
        Pair<ProjectVersion, JSONObject> response = createArtifact(projectName, artifactName);
        ProjectVersion projectVersion = response.getValue0();

        // VP - Verify that artifact exists
        assertArtifactExists(projectVersion, artifactName);
        verifyArtifactBodyStatus(projectVersion, artifactName);

        // Step - Delete artifact
        JSONObject artifactJson = response.getValue1();
        commit(CommitBuilder
            .withVersion(projectVersion)
            .withRemovedArtifact(artifactJson));

        // VP - Verify artifact does not exist
        Optional<ArtifactVersion> artifactBody =
            this.artifactVersionRepository.findByProjectVersionAndArtifactName(projectVersion, artifactName);
        assertThat(artifactBody.isPresent()).isTrue();
        ModificationType modificationType = artifactBody.get().getModificationType();
        assertThat(modificationType).isEqualTo(ModificationType.REMOVED);
    }

    @Test
    public void testArtifactExists() throws Exception {
        String projectName = "test-project";
        String artifactName = "RE-10";
        String artifactType = "requirement";
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.checkIfArtifactExists)
            .withProject(project)
            .withArtifactName(artifactName)
            .get();

        // VP - Verify that status is okay and artifact does not exist
        JSONObject response = sendGet(url, status().isOk());
        boolean artifactExists = response.getJSONObject("body").getBoolean("artifactExists");
        assertThat(artifactExists).isFalse();

        // Step - Create artifact
        dbEntityBuilder
            .newType(projectName, artifactType)
            .newArtifact(projectName, artifactType, artifactName);

        // VP - Verify that status is okay and artifact does not exist
        response = sendGet(url, status().isOk());
        artifactExists = response.getJSONObject("body").getBoolean("artifactExists");
        assertThat(artifactExists).isTrue();
    }

    private Pair<ProjectVersion, JSONObject> createArtifact(String projectName,
                                                            String artifactName) throws Exception {
        // Step - Create project with single version
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Create Artifact JSON
        JSONObject artifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifactAndReturn(projectName, "", artifactName, "requirements", "this is a body");

        // Step - Send request to create artifact
        commit(CommitBuilder
            .withVersion(projectVersion)
            .withAddedArtifact(artifactJson));
        String artifactId =
            this.artifactRepository
                .findByProjectAndName(projectVersion.getProject(), artifactName)
                .get()
                .getArtifactId()
                .toString();
        artifactJson.put("id", artifactId);

        return new Pair<>(projectVersion, artifactJson);
    }

    private void assertArtifactExists(ProjectVersion projectVersion, String artifactName) {
        Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(projectVersion.getProject(),
            artifactName);
        assertThat(artifactQuery.isPresent()).isEqualTo(true);
    }

    private void verifyArtifactBodyStatus(ProjectVersion projectVersion, String artifactName) {
        Optional<ArtifactVersion> artifactBody =
            this.artifactVersionRepository.findByProjectVersionAndArtifactName(projectVersion, artifactName);
        assertThat(artifactBody.isPresent()).isEqualTo(true);
    }
}
