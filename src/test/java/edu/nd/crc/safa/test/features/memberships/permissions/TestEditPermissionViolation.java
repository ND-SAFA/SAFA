package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;

/**
 * Verifies that users with view permissions cannot edit project.
 */
public class TestEditPermissionViolation extends AbstractPermissionViolationTest {

    @Override
    protected JSONObject performViolatingAction() throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.DELETE_PROJECT_BY_ID)
            .withProject(project)
            .deleteWithJsonObject(status().is4xxClientError());
    }

    @Override
    protected ProjectRole getExpectedRole() {
        return ProjectRole.OWNER;
    }

    @Override
    public ProjectRole getShareePermission() {
        return ProjectRole.EDITOR;
    }
}
