package edu.nd.crc.safa.test.features.github;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;
import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestGithubPermissions extends AbstractPermissionViolationTest {

    @MockBean
    private GithubConnectionService mockGithubConnectionService;

    @MockBean
    private GithubGraphQlService mockGithubGraphqlService;

    @BeforeEach
    public void setup() {
        Mockito.doReturn(Optional.of(new GithubAccessCredentials()))
            .when(mockGithubConnectionService).getGithubCredentials(Mockito.any());
    }

    @Test
    public void testFirstImport() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
                .withVersion(projectVersion)
                .withRepositoryName("repo")
                .withOwner("owner")
                .postWithJsonObject(new JSONObject() , status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS)
        );
    }

    @Test
    public void testReimport() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Github.Import.UPDATE)
                .withVersion(projectVersion)
                .withRepositoryName("repo")
                .withOwner("owner")
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS)
        );
    }
}
