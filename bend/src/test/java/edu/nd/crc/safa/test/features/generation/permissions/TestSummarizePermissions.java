package edu.nd.crc.safa.test.features.generation.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.generation.summary.ProjectSummaryService;
import edu.nd.crc.safa.features.generation.summary.SummarizeArtifactRequestDTO;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestSummarizePermissions extends AbstractPermissionViolationTest {
    @MockBean
    private ProjectSummaryService projectSummaryService;

    @MockBean
    private SummaryService summaryService;

    @Test
    public void testSummarizeArtifacts() {
        SummarizeArtifactRequestDTO body = new SummarizeArtifactRequestDTO();
        body.setArtifacts(new ArrayList<>());
        body.getArtifacts().add(UUID.randomUUID());

        test(
            () -> SafaRequest.withRoute(AppRoutes.Summarize.SUMMARIZE_ARTIFACTS)
                .withVersion(projectVersion)
                .postWithJsonObject(body, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE)
        );
    }

    @Test
    public void testSummarizeProject() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Summarize.SUMMARIZE_PROJECT)
                .withVersion(projectVersion)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE)
        );
    }
}
