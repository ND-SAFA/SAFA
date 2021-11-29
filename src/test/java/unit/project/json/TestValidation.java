package unit.project.json;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that each entity present in ProjectAppEntity is validated upon parsing.
 */
public class TestValidation extends BaseProjectJsonTest {
    /**
     * Tests that a project containing a project version but no project id is rejected.
     * TODO: Reconsider this test as we can just use the project associated with the given version.
     *
     * @throws Exception Throws exception is http request fails.
     */
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
     * Attempts to update it without including a project version.
     *
     * @throws Exception Throws exception is update request fails.
     */
    @Test
    public void attemptUpdateWithoutVersionId() throws Exception {
        // Step - Create an empty project and version.
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(user, projectName)
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
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(user, projectName)
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
     * Builds the project payload with possible missing values by not including a property if given null.
     *
     * @param name        The name of the project.
     * @param description The project description.
     * @param artifacts   The artifacts of the project.
     * @param traces      The trace links of the project.
     * @return JSONObject representing a ProjectAppEntity
     * @throws Exception Throws exception if http request fails.
     */
    private JSONObject buildProjectValidationRequest(
        String name,
        String description,
        List<JSONObject> artifacts,
        List<JSONObject> traces) throws Exception {
        // Step - Setup constants
        String url = AppRoutes.projects;
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
}
