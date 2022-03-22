package unit.project.documents;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that the client is create a new document for a project.
 */
public class CreateNewDocument extends DocumentBaseTest {

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    public void testCreateNewDocument() throws Exception {
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Create new document payload
        JSONObject docJson = jsonBuilder.createDocument(docName, docDescription, docType);

        // Step - Send creation request.
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, docJson);

        // VP - Assert all properties were returned as inputted.
        assertObjectsMatch(docJson, docCreated, List.of("documentId"));
        assertThat(docCreated.getString("documentId")).isNotEmpty();

        // VP - Verify that contents was persisted.
        assertDocumentInProjectExists(projectVersion.getProject(), docName, docDescription, docType);
    }
}
