package unit.project.currentDocument;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that a user is able to set the current document, retrieve it, and remove it.
 */
public class TestCreateRetrieveDeleteCurrentDocument extends ApplicationBaseTest {

    @Test
    public void createRetrieveDeleteDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-doc";
        String docDescription = "test-doc-description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create project, document, and version
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newDocument(projectName, docName, docDescription, docType)
            .newVersionWithReturn(projectName);
        Document document = this.dbEntityBuilder.getDocument(projectName, docName);

        // VP - Verify that currentDocumentId is null
        assertThat(getCurrentDocumentId(projectVersion)).isNull();

        // Step - Set current document
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Documents.setCurrentDocument)
            .withDocument(document)
            .buildEndpoint();
        sendPost(route, new JSONObject());

        // VP - Verify the currentDocumentId is set to document created
        assertThat(getCurrentDocumentId(projectVersion)).isEqualTo(document.getDocumentId().toString());

        // Step - Delete currentDocumentId
        String deleteRoute = RouteBuilder.withRoute(AppRoutes.Projects.Documents.clearCurrentDocument).buildEndpoint();
        sendDelete(deleteRoute);

        // VP - Verify that currentDocumentId is back to null
        assertThat(getCurrentDocumentId(projectVersion)).isNull();
    }

    public String getCurrentDocumentId(ProjectVersion projectVersion) {
        return getProjectAtVersion(projectVersion).currentDocumentId;
    }
}
