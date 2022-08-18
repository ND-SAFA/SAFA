package features.documents.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import features.documents.base.AbstractDocumentTest;
import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that the client is create a new document for a project.
 */
class TestCreateDocument extends AbstractDocumentTest {

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    void testCreateDocument() throws Exception {

        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create new document payload
        JSONObject documentJson = jsonBuilder.createDocument(docName, docDescription, docType);

        // Step - Create new document
        Pair<ProjectVersion, JSONObject> response = creationTestService.createProjectWithDocument(
            projectName,
            documentJson);

        // Step - Retrieve project version, json sent for creation, response
        ProjectVersion projectVersion = response.getValue0();
        JSONObject documentCreated = response.getValue1();

        // VP - Assert all properties were returned as inputted.
        assertionTestService.assertObjectsMatch(documentJson, documentCreated, List.of("documentId"));
        assertThat(documentCreated.getString("documentId")).isNotEmpty();

        // VP - Verify that contents was persisted.
        assertDocumentInProjectExists(projectVersion.getProject(), docName, docDescription, docType);
    }
}
