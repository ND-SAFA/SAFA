package edu.nd.crc.safa.test.features.projects;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

public class TestProjectPermissions extends AbstractPermissionViolationTest {

    @Test
    public void testUpdateProject() {
        ProjectAppEntity projectDefinition = new ProjectAppEntity();
        projectDefinition.setProjectId(project.getProjectId());

        test(
            () -> SafaRequest.withRoute(AppRoutes.Projects.CREATE_OR_UPDATE_PROJECT_META)
                .putWithJsonObject(projectDefinition, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT)
        );
    }

    @Test
    public void testDeleteProject() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Projects.DELETE_PROJECT_BY_ID)
                .withProject(project)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.DELETE, TeamPermission.DELETE_PROJECTS)
        );
    }
}
