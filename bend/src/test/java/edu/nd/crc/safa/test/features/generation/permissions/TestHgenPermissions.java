package edu.nd.crc.safa.test.features.generation.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.generation.summary.ProjectSummaryService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestHgenPermissions extends AbstractPermissionViolationTest {

    @MockBean
    private HGenService mockHgenService;

    @MockBean
    private ProjectSummaryService projectSummaryService;

    @Test
    public void testGenerateHierarchy() {
        HGenRequest body = new HGenRequest();
        test(
            () -> SafaRequest.withRoute(AppRoutes.HGen.GENERATE)
                .withVersion(projectVersion)
                .postWithJsonObject(body, status().is4xxClientError()),
            Set.of(ProjectPermission.GENERATE, ProjectPermission.EDIT_DATA)
        );
    }
}
