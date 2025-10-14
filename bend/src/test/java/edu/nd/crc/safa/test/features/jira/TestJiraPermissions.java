package edu.nd.crc.safa.test.features.jira;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jira.services.JiraParsingService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestJiraPermissions extends AbstractPermissionViolationTest {

    @MockBean
    private JiraConnectionService mockJiraConnectionService;

    @MockBean
    private JiraParsingService mockJiraParsingService;

    @Test
    public void testFirstImport() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jira.Import.IMPORT_INTO_EXISTING)
                .withVersion(projectVersion)
                .withOrgId(UUID.randomUUID())
                .withPathVariable("id", "0")
                .postWithJsonObject(new JSONObject() , status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS)
        );
    }

    @Test
    public void testReimport() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jira.Import.UPDATE)
                .withVersion(projectVersion)
                .withOrgId(UUID.randomUUID())
                .withPathVariable("id", "0")
                .putWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS)
        );
    }
}
