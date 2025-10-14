package edu.nd.crc.safa.test.features.traces.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestTraceMatrixPermissions extends AbstractPermissionViolationTest {

    @Test
    public void testNewEntry() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.TraceMatrix.BY_SOURCE_AND_TARGET_TYPES)
                .withPathVariable("projectVersionId", projectVersion.getVersionId().toString())
                .withPathVariable("sourceTypeName", "sourceType")
                .withPathVariable("targetTypeName", "targetType")
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testDeleteEntryByTypeNames() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.TraceMatrix.BY_SOURCE_AND_TARGET_TYPES)
                .withPathVariable("projectVersionId", projectVersion.getVersionId().toString())
                .withPathVariable("sourceTypeName", "sourceType")
                .withPathVariable("targetTypeName", "targetType")
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testDeleteEntryById() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.TraceMatrix.BY_ID)
                .withPathVariable("projectVersionId", projectVersion.getVersionId().toString())
                .withPathVariable("traceMatrixId", UUID.randomUUID().toString())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }
}
