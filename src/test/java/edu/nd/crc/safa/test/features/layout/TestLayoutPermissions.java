package edu.nd.crc.safa.test.features.layout;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.layout.entities.api.LayoutGenerationRequestDTO;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

public class TestLayoutPermissions extends AbstractPermissionViolationTest {

    @Test
    public void testRegenerateLayout() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Layout.REGENERATE_LAYOUT)
                .withVersion(projectVersion)
                .postWithJsonObject(new LayoutGenerationRequestDTO(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }
}
