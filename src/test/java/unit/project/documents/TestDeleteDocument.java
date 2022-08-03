package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that a user is able to delete a document in a project.
 */
class TestDeleteDocument extends ApplicationBaseTest {

    /**
     * Verifies that a document can be deleted by a user.
     */
    @Test
    void testDeleteOnlyDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docDescription = "this is a description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create project containing a single document.
        Document document = dbEntityBuilder
            .newProject(projectName)
            .newDocument(projectName, docName, docDescription, docType)
            .getDocument(projectName, docName);
        Project project = dbEntityBuilder.getProject(projectName);

        // Step - Create new document payload
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Documents.DELETE_DOCUMENT)
            .withDocument(document)
            .buildEndpoint();
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Verify that no documents are associated with project
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        assertThat(projectDocuments.size()).isZero();
    }
}
