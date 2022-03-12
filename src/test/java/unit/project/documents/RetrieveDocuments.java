package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that a user is able to delete a document in a project.
 */
public class RetrieveDocuments extends ApplicationBaseTest {

    /**
     * Verifies that a document can be deleted by a user.
     */
    @Test
    public void testGetProjectDocuments() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docNameTwo = "test-another-doc";
        String docDescription = "this is a description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Retrieve project documents
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.Documents.getProjectDocuments)
            .withProject(project)
            .get();
        JSONArray documents = sendGetWithArrayResponse(route, status().isOk());

        // VP - Verify that no documents are returned
        assertThat(documents.length()).isEqualTo(0);

        // Step - Create two documents.
        dbEntityBuilder
            .newDocument(projectName, docName, docDescription, docType)
            .newDocument(projectName, docNameTwo, docDescription, docType);

        // Step - Retrieve project documents
        documents = sendGetWithArrayResponse(route, status().isOk());

        // VP - Verify that no documents are associated with project
        assertThat(documents.length()).isEqualTo(2);
    }
}
