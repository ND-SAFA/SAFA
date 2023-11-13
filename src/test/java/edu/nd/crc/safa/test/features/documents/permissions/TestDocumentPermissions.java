package edu.nd.crc.safa.test.features.documents.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestDocumentPermissions extends AbstractPermissionViolationTest {

    private Document document;

    @BeforeEach
    public void testSetup() {
        document =
            dbEntityBuilder
                .newDocument(projectName, "document", "description")
                .getDocument(projectName, "document");
    }

    @Test
    public void testDeleteDocument() {
        test(
            () -> SafaRequest
                .withRoute(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
                .withDocument(document)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testCreateDocument() {
        test(
            () -> {
                DocumentAppEntity document = new DocumentAppEntity();
                document.setName("name");
                document.setDescription("description");

                return SafaRequest
                    .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
                    .withVersion(projectVersion)
                    .postWithJsonObject(document, status().is4xxClientError());
            },
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

}
