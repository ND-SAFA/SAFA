package edu.nd.crc.safa.test.features.projects.json;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;

/**
 * Creates a constant environment and functions for creating or updating projects
 * via the JSON route.
 */
public abstract class AbstractProjectJsonTest extends ApplicationBaseTest {
    protected final int N_TYPES = 2;
    protected final int N_ARTIFACTS = 2;
    protected final int N_TRACES = 1;
    protected final String a1Type = "requirement";
    protected final String a1Name = "RE-8";
    protected final String a1Body = "this is a requirement";
    protected final String a2Type = "design";
    protected final String a2Name = "DD-10";
    protected final String a2Body = "this is a design";
    protected final String projectName = "test-project";
    protected final String projectDescription = "test-description";

    protected JSONObject postProjectJson(JSONObject projectJson) throws Exception {
        return postProjectJson(projectJson, status().isCreated());
    }

    protected JSONObject postProjectJson(JSONObject projectJson,
                                         ResultMatcher expectedStatus) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
            .postWithJsonObject(projectJson, expectedStatus);
    }

    protected JSONObject putProjectJson(JSONObject projectJson) throws Exception {
        return putProjectJson(projectJson, status().is2xxSuccessful());
    }

    protected JSONObject putProjectJson(JSONObject projectJson,
                                        ResultMatcher expectedStatus) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
            .putWithJsonObject(projectJson, expectedStatus);
    }

    /**
     * Creates a project containing two artifacts and a trace link between them.
     * The artifacts are of type requirement and design.
     *
     * @return JSONObject formatted for a ProjectAppEntity
     */
    protected JSONObject createBaseProjectJson() {
        return createBaseProjectJson(null, a1Body, null, a2Body);

    }

    private JSONObject createBaseProjectJson(UUID a1Id, String a1Body, UUID a2Id, String a2Body) {
        return jsonBuilder
            .withProject("", projectName, projectDescription)
            .withArtifact(projectName, a1Id, a1Name, a1Type, a1Body)
            .withArtifact(projectName, a2Id, a2Name, a2Type, a2Body)
            .withTrace(projectName, a1Name, a2Name)
            .getProjectJson(projectName);
    }

    protected void verifyProjectInformation(UUID projectId, String name, String description) {
        Project updatedProject = this.projectRepository.findByProjectId(projectId);
        assertThat(updatedProject.getName()).isEqualTo(name);
        assertThat(updatedProject.getDescription()).isEqualTo(description);
    }
}
