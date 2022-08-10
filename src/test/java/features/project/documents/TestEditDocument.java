package unit.project.documents;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that the client can edit an existing document.
 */
class TestEditDocument extends DocumentBaseTest {

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    void testEditDescription() throws Exception {
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
        assertObjectsMatch(docJson, docCreated);

        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType);
    }

    /**
     * Verifies that a new document can be created for a project.
     */
    @Test
    void testDeleteArtifactIds() throws Exception {
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
        JSONObject docRequestJson = jsonBuilder.createDocument(docName, newDescription, docType);
        docRequestJson.put("documentId", document.getDocumentId().toString());
        Artifact artifact = this.dbEntityBuilder.getArtifact(projectName, artifactName);
        List<String> artifactIds = List.of(artifact.getArtifactId().toString());
        docRequestJson.put("artifactIds", artifactIds);

        // Step - Send Update request.
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, docRequestJson);

        // VP - Verify that response object contains name, description, and type
        assertObjectsMatch(docRequestJson, docCreated, List.of("documentId"));
        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType, artifactIds);

        // Step - Delete artifact id
        artifactIds = new ArrayList<>();
        docRequestJson.put("artifactIds", artifactIds);

        // Step - Update document
        JSONObject docUpdated = createOrUpdateDocumentJson(projectVersion, docRequestJson);

        // VP - Verify that response contains updates.
        assertObjectsMatch(docRequestJson, docUpdated);
        assertDocumentInProjectExists(projectVersion.getProject(), docName, newDescription, docType, artifactIds);
    }
}
