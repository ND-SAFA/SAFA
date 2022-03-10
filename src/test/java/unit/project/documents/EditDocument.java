package unit.project.documents;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.server.entities.db.Artifact;
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
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, docJson);

        // VP - Verify that response object contains name, description, and type
        assertObjectsMatch(docCreated, docJson);

        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType);
    }

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    public void testDeleteArtifactIds() throws Exception {
        String newDescription = "this is another description";
        String artifactName = "RE-10";
        String artifactType = "requirement";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        // Step - Create empty project
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newDocument(projectName, docName, docDescription, DocumentType.SAFETY_CASE)
            .newType(projectName, artifactType)
            .newArtifact(projectName, artifactType, artifactName)
            .newVersionWithReturn(projectName);
        Document document = dbEntityBuilder.getDocument(projectName, docName);

        // Step - Create new document payload
        JSONObject docJson = jsonBuilder.createDocument(docName, newDescription, docType);
        docJson.put("documentId", document.getDocumentId().toString());
        Artifact artifact = this.dbEntityBuilder.getArtifact(projectName, artifactName);
        List<String> artifactIds = List.of(artifact.getArtifactId().toString());
        docJson.put("artifactIds", artifactIds);

        // Step - Send Update request.
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, docJson);

        // VP - Verify that response object contains name, description, and type
        assertObjectsMatch(docCreated, docJson);
        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType, artifactIds);

        // Step - Delete artifact id
        artifactIds = new ArrayList<>();
        docJson.put("artifactIds", artifactIds);

        // Step - Update document
        JSONObject docUpdated = createOrUpdateDocumentJson(projectVersion, docJson);

        // VP - Verify that response contains updates.
        assertObjectsMatch(docJson, docUpdated);
        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType, artifactIds);

        // VP - Verify that updates are persisted
        System.out.println("NUMBER LINKED ARTIFACTS" + this.documentArtifactRepository.findByDocument(document).size());

    }
}
