package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;

public class TestCreateDocumentPermissionViolation extends AbstractPermissionViolationTest {

    @Override
    protected JSONObject performViolatingAction() {
        DocumentAppEntity document = new DocumentAppEntity();
        document.setName("name");
        document.setDescription("description");

        return SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(document, status().is4xxClientError());
    }

    @Override
    protected Set<Permission> getExpectedPermissions() {
        return Set.of(ProjectPermission.EDIT_DATA);
    }
}
