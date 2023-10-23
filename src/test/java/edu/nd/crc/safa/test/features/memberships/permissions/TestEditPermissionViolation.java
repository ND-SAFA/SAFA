package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
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
    protected Set<Permission> getExpectedPermissions() {
        return Set.of(ProjectPermission.DELETE, TeamPermission.DELETE_PROJECTS);
    }

    @Override
    public ProjectRole getShareePermission() {
        return ProjectRole.EDITOR;
    }
}
