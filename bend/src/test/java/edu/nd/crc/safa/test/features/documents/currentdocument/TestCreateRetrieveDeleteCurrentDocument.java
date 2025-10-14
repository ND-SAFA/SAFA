package edu.nd.crc.safa.test.features.documents.currentdocument;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.RouteBuilder;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that a user is able to set the current document, retrieve it, and remove it.
 */
class TestCreateRetrieveDeleteCurrentDocument extends ApplicationBaseTest {

    @Test
    void createRetrieveDeleteDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-doc";
        String docDescription = "test-doc-description";

        // Step - Create project, document, and version
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newDocument(projectName, docName, docDescription)
            .newVersionWithReturn(projectName);
        Document document = this.dbEntityBuilder.getDocument(projectName, docName);

        // VP - Verify that currentDocumentId is null
        assertThat(getCurrentDocumentId(projectVersion)).isNull();

        // Step - Set current document
        SafaRequest
            .withRoute(AppRoutes.Documents.SET_CURRENT_DOCUMENT)
            .withDocument(document)
            .postWithJsonObject(new JSONObject());

        // VP - Verify the currentDocumentId is set to document created
        assertThat(getCurrentDocumentId(projectVersion)).isEqualTo(document.getDocumentId().toString());

        // Step - Delete currentDocumentId
        String deleteRoute = RouteBuilder.withRoute(AppRoutes.Documents.CLEAR_CURRENT_DOCUMENT).buildEndpoint();
        SafaRequest.withRoute(deleteRoute).deleteWithJsonObject();

        // VP - Verify that currentDocumentId is back to null
        assertThat(getCurrentDocumentId(projectVersion)).isNull();
    }

    String getCurrentDocumentId(ProjectVersion projectVersion) {
        return retrievalService.getProjectAtVersion(projectVersion).getCurrentDocumentId();
    }
}
