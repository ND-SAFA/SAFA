package unit.controllers.project;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;
import unit.EntityBaseTest;

/**
 * Tests that /projects/ is able to create new projects from the front-end
 * JSON representation as well as updates the elements if they already exists
 */
public class TestProjectCreateOrUpdateJson extends EntityBaseTest {

    final int N_TYPES = 2;
    final int N_ARTIFACTS = 2;
    final int N_TRACES = 1;
    final String a1Type = "requirement";
    final String a1Name = "RE-8";
    final String a2Type = "design";
    final String a2Name = "DD-10";
    final String projectName = "test-project";
    final String routeName = "/projects/";

    @Autowired
    ObjectMapper objectMapper;

    /**
     * Tests that all entities in the given request created. Namely,
     * - a source artifact + requirement type
     * - a target artifact + design type
     * - a trace link (between artifacts)
     */
    @Test
    public void createEntitiesFromJson() throws Exception {
        JSONObject projectJson = createProjectJson();
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getJSONObject("body")
            .getJSONObject("project")
            .getString("projectId");
        Project project = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        testProjectArtifactsCreated(project, 1);
        projectService.deleteProject(project);
    }

    /**
     * Sends a request to the same api with a new project name and
     * an updated artifact body. Expects all entities to remain in
     * the database and have only updated the entities given.
     */
    @Test
    public void updateEntities() throws Exception {
        // Step - Create Basic Project (repeat of createEntitiesFromJson)
        JSONObject projectJson = createProjectJson();
        JSONObject responseContent = postProjectJson(projectJson);
        String projectId = responseContent
            .getJSONObject("body")
            .getJSONObject("project")
            .getString("projectId");
        String versionId = responseContent
            .getJSONObject("body")
            .getJSONObject("projectVersion")
            .getString("versionId");
        Project project = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        testProjectArtifactsCreated(project, 1);
        List<ArtifactBody> artifactBodiesQuery =
            this.artifactBodyRepository.getBodiesWithName(project, a1Name);
        assertThat(artifactBodiesQuery.size()).as("# of bodies on init").isEqualTo(1);

        // Step - Create Updated Request and Send
        String newProjectName = "new-project-name";
        String newArtifactBody = "new-artifact-body";
        JSONObject updateRequestJson = jsonBuilder
            .withProject(projectId, newProjectName)
            .withProjectVersion(newProjectName, versionId, 1, 1, 2)
            .withArtifact(newProjectName, a1Name, a1Type, newArtifactBody)
            .getPayload(newProjectName);
        postProjectJson(updateRequestJson);

        // VP - Verify that project name has changed
        Project updatedProject = this.projectRepository.findByProjectId(UUID.fromString(projectId));
        assertThat(updatedProject.getName()).isEqualTo(newProjectName);
        // VP - Verify that entities still exist and no other version was created
        testProjectArtifactsCreated(project, 1);
        // VP - Verify that artifact has two versions and the latest has updated body.
        artifactBodiesQuery =
            this.artifactBodyRepository.getBodiesWithName(project, a1Name);
        assertThat(artifactBodiesQuery.size()).as("# of bodies on update").isEqualTo(1);
        assertThat(artifactBodiesQuery.get(0).getContent()).isEqualTo(newArtifactBody);
    }

    private void testProjectArtifactsCreated(Project project, int expectedVersions) {
        // VP - Resources were created
        List<ProjectVersion> projectVersions = projectVersionRepository.findByProject(project);
        assertThat(projectVersions.size()).as("# versions").isEqualTo(expectedVersions);
        ProjectVersion projectVersion = projectVersions.get(0);
        assertThat(projectVersion).as("project version created").isNotNull();

        // VP - Project types are created
        List<ArtifactType> projectTypes = artifactTypeRepository.findByProject(project);
        assertThat(projectTypes.size()).as("all types created").isEqualTo(N_TYPES);

        // VP - requirements created
        Optional<ArtifactType> requirementType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "requirement");
        assertThat(requirementType.isPresent()).as("requirement type created").isTrue();
        List<Artifact> requirements = artifactRepository.findByProjectAndType(project, requirementType.get());
        assertThat(requirements.size()).as("requirements created").isEqualTo(1);

        // VP - design definitions created
        Optional<ArtifactType> designType = artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, "design");
        assertThat(designType.isPresent()).as("design type created").isTrue();
        List<Artifact> designs = artifactRepository.findByProjectAndType(project, designType.get());
        assertThat(designs.size())
            .as("designs created)")
            .isEqualTo(1);

        List<Artifact> projectArtifacts = artifactRepository.findByProject(project);
        assertThat(projectArtifacts.size()).isEqualTo(N_ARTIFACTS);

        // VP - Artifact bodies
        List<ArtifactBody> artifactBodies = artifactBodyRepository.findByProjectVersion(projectVersion);
        assertThat(artifactBodies.size())
            .as("artifact bodies created")
            .isEqualTo(N_ARTIFACTS);
        List<TraceLink> traceLinks = traceLinkRepository.getApprovedLinks(project);
        assertThat(traceLinks.size()).isEqualTo(N_TRACES);
    }

    @Test
    public void attemptToUpdateProjectWithoutProjectId() throws Exception {
        String mockVersionId = UUID.randomUUID().toString();
        JSONObject payload = jsonBuilder
            .withProject("", projectName)
            .withArtifact(projectName, a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, mockVersionId, 1, 1, 1)
            .getPayload(projectName);

        JSONObject response = postProjectJson(payload, status().is4xxClientError());
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).contains("Invalid ProjectVersion");
    }

    @Test
    public void attemptUpdateWithoutVersionId() throws Exception {
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        String projectId = projectVersion.getProject().getProjectId().toString();
        JSONObject payload = jsonBuilder
            .withProject(projectId, projectName)
            .withArtifact(projectName, a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, "", 1, 1, 1)
            .getPayload(projectName);

        JSONObject response = postProjectJson(payload, status().is4xxClientError());
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).contains("valid ID");
    }

    @Test
    public void attemptUpdateWithoutValidVersionNumber() throws Exception {
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        String projectId = projectVersion.getProject().getProjectId().toString();
        String mockVersionId = UUID.randomUUID().toString();
        JSONObject payload = jsonBuilder
            .withProject(projectId, projectName)
            .withArtifact(projectName, a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, mockVersionId, 0, 0, 0)
            .getPayload(projectName);

        JSONObject response = postProjectJson(payload, status().is4xxClientError());
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).contains("positive major");
    }

    private JSONObject postProjectJson(JSONObject projectJson) throws Exception {
        return postProjectJson(projectJson, status().isCreated());
    }

    private JSONObject postProjectJson(JSONObject projectJson,
                                       ResultMatcher expectedStatus) throws Exception {
        return sendPost(routeName, projectJson, expectedStatus);
    }

    private JSONObject createProjectJson() {
        return jsonBuilder
            .withProject("", projectName)
            .withArtifact(projectName, a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, "", 1, 1, 1)
            .getPayload(projectName);
    }
}
