package edu.nd.crc.safa.test.features.versions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestVersionPermissions extends AbstractPermissionViolationTest {

    @Test
    public void testGetVersions() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.GET_VERSIONS)
                .withProject(project)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }

    @Test
    public void testGetCurrentVersion() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.GET_CURRENT_VERSION)
                .withProject(project)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }

    @Test
    public void testCreateMajorVersion() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.CREATE_NEW_MAJOR_VERSION)
                .withProject(project)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_VERSIONS)
        );
    }

    @Test
    public void testCreateMinorVersion() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.CREATE_NEW_MINOR_VERSION)
                .withProject(project)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_VERSIONS)
        );
    }

    @Test
    public void testCreateRevisionVersion() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.CREATE_NEW_REVISION_VERSION)
                .withProject(project)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_VERSIONS)
        );
    }

    @Test
    public void testDeleteVersion() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Versions.DELETE_VERSION_BY_ID)
                .withVersion(projectVersion)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_VERSIONS)
        );
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }

}
