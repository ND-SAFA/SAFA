package unit.project.documents;

import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that the client can edit an existing document.
 */
public class EditDocument extends DocumentBaseTest {

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    public void testEditDescription() throws Exception {
        String newDescription = "this is another description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newDocument(projectName, docName, docDescription, DocumentType.SAFETY_CASE)
            .newVersionWithReturn(projectName);
        Document document = dbEntityBuilder.getDocument(projectName, docName);

        // Step - Create new document payload
        JSONObject docJson = jsonBuilder.createDocument(docName, newDescription, docType);
        docJson.put("documentId", document.getDocumentId().toString());

        // Step - Send Update request.
        JSONObject docCreated = createDocument(projectVersion, docJson);

        // VP - Verify that response object contains name, description, and type
        assertObjectsMatch(docCreated, docJson);

        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType);
    }
}
