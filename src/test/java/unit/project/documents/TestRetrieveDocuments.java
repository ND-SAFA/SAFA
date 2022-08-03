package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that a user is able to retrieve a document in a project.
 */
class TestRetrieveDocuments extends DocumentBaseTest {

    /**
     * Verifies that a document can be deleted by a user.
     */
    @Test
    void testGetProjectDocuments() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docNameTwo = "test-another-doc";
        String docDescription = "this is a description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Retrieve project documents
        JSONArray documents = getProjectDocuments(project);

        // VP - Verify that no documents are returned
        assertThat(documents.length()).isZero();

        // Step - Create two documents.
        dbEntityBuilder
            .newDocument(projectName, docName, docDescription, docType)
            .newDocument(projectName, docNameTwo, docDescription, docType);

        // Step - Retrieve project documents
        documents = getProjectDocuments(project);

        // VP - Verify that no documents are associated with project
        assertThat(documents.length()).isEqualTo(2);
    }
}
