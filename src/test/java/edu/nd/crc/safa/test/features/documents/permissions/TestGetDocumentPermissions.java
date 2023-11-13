package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestGetDocumentPermissions extends AbstractPermissionViolationTest {

    private Document document;

    @BeforeEach
    public void testSetup() {
        document =
            dbEntityBuilder
                .newDocument(projectName, "document", "description")
                .getDocument(projectName, "document");
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }

    @Test
    public void testGetDocument() {
        test(
            () -> SafaRequest
                .withRoute(AppRoutes.Documents.GET_DOCUMENT_BY_ID)
                .withVersion(projectVersion)
                .withDocument(document)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }

    @Test
    public void testGetProjectDocuments() {
        test(
            () -> SafaRequest
                .withRoute(AppRoutes.Documents.GET_PROJECT_DOCUMENTS)
                .withVersion(projectVersion)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }
}
