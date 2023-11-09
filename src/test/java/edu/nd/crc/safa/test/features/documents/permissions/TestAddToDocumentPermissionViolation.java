package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;

public class TestAddToDocumentPermissionViolation extends AbstractPermissionViolationTest {

    private Document document;

    @BeforeEach
    public void testSetup() {
        document =
            dbEntityBuilder
                .newDocument(projectName, "document", "description")
                .getDocument(projectName, "document");
    }

    @Override
    protected JSONObject performViolatingAction() {
        return SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .postWithJsonObject(new JSONArray(), status().is4xxClientError());
    }

    @Override
    protected Set<Permission> getExpectedPermissions() {
        return Set.of(ProjectPermission.EDIT_DATA);
    }
}
