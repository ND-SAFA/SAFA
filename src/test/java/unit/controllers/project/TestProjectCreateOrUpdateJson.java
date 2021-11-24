package unit.controllers.project;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;
import unit.ApplicationBaseTest;

/**
 * Tests that user is able to create new projects from the front-end
 * JSON representation as well as updates the elements if they already exists
 */
public class TestProjectCreateOrUpdateJson extends ApplicationBaseTest {

    final int N_TYPES = 2;
    final int N_ARTIFACTS = 2;
    final int N_TRACES = 1;
    final String a1Type = "requirement";
    final String a1Name = "RE-8";
    final String a2Type = "design";
    final String a2Name = "DD-10";
    final String projectName = "test-project";
    final String projectDescription = "test-description";

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
        JSONObject projectJson = createBaseProjectJson();
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
     * Test that user is able to update project with checks for:
     */
    @Test
    public void updateEntities() throws Exception {
        // Step - Create Project containing:
        JSONObject projectJson = createBaseProjectJson();
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
        String artifactId = artifactBodiesQuery.get(0).getArtifact().getArtifactId().toString();
        JSONObject updateRequestJson = jsonBuilder
            .withProject(projectId, newProjectName, projectDescription)
            .withProjectVersion(newProjectName, versionId, 1, 1, 2)
            .withArtifact(newProjectName, artifactId, a1Name, a1Type, newArtifactBody)
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

        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(project);
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
    public void attemptToUpdateProjectWithEmptyProjectId() throws Exception {
        String mockVersionId = UUID.randomUUID().toString();
        JSONObject payload = jsonBuilder
            .withProject("", projectName, projectDescription)
            .withArtifact(projectName, "", a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, "", a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, mockVersionId, 1, 1, 1)
            .getPayload(projectName);

        JSONObject response = postProjectJson(payload, status().is4xxClientError());
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).contains("Invalid ProjectVersion");
    }

    /**
     * Creates a project and attempts to update it without including a project version.
     *
     * @throws Exception Throws exception is update request fails.
     */
    @Test
    public void attemptUpdateWithoutVersionId() throws Exception {
        // Step - Create an empty project and version.
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        String projectId = projectVersion.getProject().getProjectId().toString();

        // Step - Create an update project payload containing two artifacts and a trace links between them.
        JSONObject payload = jsonBuilder
            .withProject(projectId, projectName, projectDescription)
            .withArtifact(projectName, "", a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, "", a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .withProjectVersion(projectName, "", 1, 1, 1)
            .getPayload(projectName);

        // Step - Send update request
        JSONObject response = postProjectJson(payload, status().is4xxClientError());

        // VP - Verify that the error message is about project version id
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).matches(".*versionId.*not.*null[\\s\\S]");
    }

    /**
     * Tests that the project version validation is activated by sending an invalid project version
     * containing a negative minor version.
     *
     * @throws Exception Throws exception is post request fails.
     */
    @Test
    public void testProjectVersionValidation() throws Exception {
        // Step - Create project and version.
        ProjectVersion projectVersion = entityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        String projectId = projectVersion.getProject().getProjectId().toString();
        String mockVersionId = UUID.randomUUID().toString();

        // Step - Create JSON payload containing 2 artifacts, a trace, and an invalid major version number .
        JSONObject payload = jsonBuilder
            .withProject(projectId, projectName, projectDescription)
            .withProjectVersion(projectName, mockVersionId, 1, -1, 0)
            .getPayload(projectName);

        // Step - Send project creation request
        JSONObject response = postProjectJson(payload, status().is4xxClientError());

        // VP - Verify that minor version is the error received
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).contains("minorVersion").contains("greater than 0");
    }

    /**
     * Tests that a project description must be defined, even if empty.
     *
     * @throws Exception Throws exception is post request fails.
     */
    @Test
    public void testProjectIdentifierValidation() throws Exception {
        JSONObject response = buildProjectValidationRequest(null, new ArrayList<>(), new ArrayList<>());
        JSONObject body = response.getJSONObject("body");
        assertThat(response.getNumber("status")).isEqualTo(1);
        assertThat(body.getString("message")).matches(".*name.*not.*null[\\s\\S]");
    }

    /**
     * Tests that artifact are validated automatically in project payload.
     * 1. Artifacts are not null
     * 2. Each artifact is triggering the validation flags.
     *
     * @throws Exception Throws exception is a problem occurred while sending a http message.
     */
    @Test
    public void testArtifactValidation() throws Exception {
        // Step - Create invalid artifact - empty type name
        JSONObject invalidArtifact = jsonBuilder
            .withProject(projectName, projectName, projectDescription)
            .withArtifactAndReturn(projectName, "", "RE-1", "", "");

        // Step - Send creation request
        JSONObject response = buildProjectValidationRequest(
            "artifact-validation",
            List.of(invalidArtifact),
            new ArrayList<>());

        // VP - Assert that message indicates that artifact validation was triggered.
        JSONObject body = response.getJSONObject("body");
        assertThat(response.getNumber("status")).isEqualTo(1);
        assertThat(body.getString("message")).contains("artifacts").contains("type");
    }

    /**
     * Tests that the TraceAppEntity validation is activated by passing invalid trace link
     *
     * @throws Exception Throws exception is project update request fails.
     */
    @Test
    public void testTraceValidation() throws Exception {
        // Step - contains
        String projectName = "trace-validation";

        // Step - Create invalid traces - missing source name
        JSONObject invalidTrace = jsonBuilder
            .withProject(projectName, projectName, projectDescription)
            .withTraceAndReturn(projectName, "", "RE-10");

        // Step - Send creation request
        JSONObject response = buildProjectValidationRequest(
            projectName,
            projectDescription,
            new ArrayList<>(),
            List.of(invalidTrace));

        // Step - Assert that message indicates that artifact validation was triggered.
        JSONObject body = response.getJSONObject("body");
        assertThat(response.getNumber("status")).isEqualTo(1);
        assertThat(body.getString("message")).matches(".*source.*not.*empty[\\s\\S]");
    }

    private JSONObject buildProjectValidationRequest(
        String projectName,
        List<JSONObject> artifacts,
        List<JSONObject> traces
    ) throws Exception {
        return buildProjectValidationRequest(projectName, projectDescription, artifacts, traces);
    }

    /**
     * Builds the project payload by not including a property if null.
     *
     * @param name        The name of the project.
     * @param description The project description.
     * @param artifacts   The artifacts of the project.
     * @param traces      The trace links of the project.
     * @return JSONObject representing a ProjectAppEntity
     * @throws Exception
     */
    private JSONObject buildProjectValidationRequest(
        String name,
        String description,
        List<JSONObject> artifacts,
        List<JSONObject> traces) throws Exception {
        // Step - Setup constants
        String url = Routes.projects;
        JSONObject projectJson = new JSONObject();

        // Step - Create project payload
        projectJson.put("projectId", "");

        if (name != null) {
            projectJson.put("name", name);
        }
        if (description != null) {
            projectJson.put("description", description);
        }
        if (artifacts != null) {
            projectJson.put("artifacts", artifacts);
        }
        if (traces != null) {
            projectJson.put("traces", traces);
        }

        return sendPost(url, projectJson, status().isBadRequest());
    }

    private JSONObject postProjectJson(JSONObject projectJson) throws Exception {
        return postProjectJson(projectJson, status().isCreated());
    }

    private JSONObject postProjectJson(JSONObject projectJson,
                                       ResultMatcher expectedStatus) throws Exception {
        return sendPost(Routes.projects, projectJson, expectedStatus);
    }

    /**
     * Creates a project containing two a requirement and design, a trace link between them, the the baseline
     * project version.
     *
     * @return JSONObject formatted for a ProjectAppEntity
     */
    private JSONObject createBaseProjectJson() {
        return jsonBuilder
            .withProject("", projectName, projectDescription)
            .withArtifact(projectName, "", a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, "", a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .getPayload(projectName);
    }
}
