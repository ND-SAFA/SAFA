package edu.nd.crc.safa.test.features.generation.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

public class TestLinkGenerationPermissions extends AbstractPermissionViolationTest {

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }

    @Test
    public void testGetGeneratedLinks() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Links.GET_GENERATED_LINKS_IN_PROJECT_VERSION)
                .withVersion(projectVersion)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }
}
