package features.documents.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.documents.base.AbstractDocumentTest;
import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that a user is able to retrieve a document in a project.
 */
class TestRetrieveDocument extends AbstractDocumentTest {

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
        ProjectVersion projectVersion = dbEntityBuilder.newVersionWithReturn(projectName);

        // Step - Retrieve project documents
        JSONArray documents = getProjectDocuments(projectVersion);

        // VP - Verify that no documents are returned
        assertThat(documents.length()).isZero();

        // Step - Create two documents.
        dbEntityBuilder
            .newDocument(projectName, docName, docDescription, docType)
            .newDocument(projectName, docNameTwo, docDescription, docType);

        // Step - Retrieve project documents
        documents = getProjectDocuments(projectVersion);

        // VP - Verify that no documents are associated with project
        assertThat(documents.length()).isEqualTo(2);
    }
}
