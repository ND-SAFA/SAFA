package edu.nd.crc.safa.test.features.types;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

public class TestTypePermissions extends AbstractPermissionViolationTest {

    @Test
    public void testCreateType() {
        ArtifactType type = new ArtifactType();
        test(
            () -> SafaRequest.withRoute(AppRoutes.ArtifactType.CREATE_ARTIFACT_TYPE)
                .withProject(project)
                .postWithJsonObject(type, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testUpdateType() {
        ArtifactType type = new ArtifactType();
        test(
            () -> SafaRequest.withRoute(AppRoutes.ArtifactType.UPDATE_ARTIFACT_TYPE)
                .withProject(project)
                .withArtifactType("type")
                .putWithJsonObject(type, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testDeleteType() {
        ArtifactType type = dbEntityBuilder.newTypeAndReturn(projectName, "typeName");
        test(
            () -> SafaRequest.withRoute(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
                .withType(type)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }
}
