package edu.nd.crc.safa.test.features.generation.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.generation.search.SearchMode;
import edu.nd.crc.safa.features.generation.search.SearchRequest;
import edu.nd.crc.safa.features.generation.search.SearchService;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestSearchPermissions extends AbstractPermissionViolationTest {

    @MockBean
    private SearchService mockSearchService;

    @Test
    public void testSearchPermissions() {
        SearchRequest body = new SearchRequest();
        body.setSearchTypes(new ArrayList<>());
        body.setMode(SearchMode.ARTIFACTS);
        test(
            () -> SafaRequest.withRoute(AppRoutes.Search.SEARCH)
                .withVersion(projectVersion)
                .postWithJsonObject(body, status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW, ProjectPermission.GENERATE)
        );
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }
}
