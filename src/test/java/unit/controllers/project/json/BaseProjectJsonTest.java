package unit.controllers.project.json;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.Routes;

import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;
import unit.ApplicationBaseTest;

/**
 * Creates a constant environment and functions for creating or updating projects
 * via the JSON route.
 */
public class BaseProjectJsonTest extends ApplicationBaseTest {
    protected final int N_TYPES = 2;
    protected final int N_ARTIFACTS = 2;
    protected final int N_TRACES = 1;
    protected final String a1Type = "requirement";
    protected final String a1Name = "RE-8";
    protected final String a2Type = "design";
    protected final String a2Name = "DD-10";
    protected final String projectName = "test-project";
    protected final String projectDescription = "test-description";

    protected JSONObject postProjectJson(JSONObject projectJson) throws Exception {
        return postProjectJson(projectJson, status().isCreated());
    }

    protected JSONObject postProjectJson(JSONObject projectJson,
                                         ResultMatcher expectedStatus) throws Exception {
        return sendPost(Routes.projects, projectJson, expectedStatus);
    }

    /**
     * Creates a project containing two a requirement and design, a trace link between them, the the baseline
     * project version.
     *
     * @return JSONObject formatted for a ProjectAppEntity
     */
    protected JSONObject createBaseProjectJson() {
        String emptyArtifactId = "";
        return jsonBuilder
            .withProject("", projectName, projectDescription)
            .withArtifact(projectName, emptyArtifactId, a1Name, a1Type, "this is a requirement")
            .withArtifact(projectName, emptyArtifactId, a2Name, a2Type, "this is a design")
            .withTrace(projectName, a1Name, a2Name)
            .getPayload(projectName);
    }
}
