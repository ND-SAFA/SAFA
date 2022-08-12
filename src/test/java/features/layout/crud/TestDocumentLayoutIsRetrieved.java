package features.layout.crud;

import java.util.List;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import features.layout.base.AbstractCorrectnessTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that nodes are formatted in a hierarchical structure.
 */
class TestDocumentLayoutIsRetrieved extends AbstractCorrectnessTest {

    @Test
    void testDocumentLayoutIsRetrieved() throws Exception {
        String documentName = "test-document";

        // Step - Create project
        JSONObject commitResponse = createProject();
        Document document = this.dbEntityBuilder
            .newDocument(projectName, documentName, "", DocumentType.ARTIFACT_TREE)
            .getDocument(projectName, documentName);

        // Step - Add artifacts to layout
        JSONArray artifactsJson = commitResponse.getJSONObject("artifacts").getJSONArray("added");
        addArtifactToDocument(projectVersion, document, artifactsJson);

        // Step - Retrieve project (including layout)
        ProjectAppEntity project = getProjectAtVersion(projectVersion);

        // Step - Extract artifact positions
        String documentId = document.getDocumentId().toString();
        LayoutPosition a1Pos = getArtifactPositionInProjectLayout(project, documentId, a1Name);
        LayoutPosition a2Pos = getArtifactPositionInProjectLayout(project, documentId, a2Name);
        LayoutPosition a3Pos = getArtifactPositionInProjectLayout(project, documentId, a3Name);

        // VP - Verify that root has greatest y
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }

    @Test
    void testDocumentLayoutOnCreation() throws Exception {
        String docName = "doc-name";
        DocumentType docType = DocumentType.ARTIFACT_TREE;
        String docDescription = "";

        // Step - Create project
        JSONObject projectCommit = createProject();
        List<String> artifactIds = getArtifactIds(projectCommit);

        // Step - Create new document payload
        JSONObject documentJson = jsonBuilder.createDocument(
            docName,
            docDescription,
            docType,
            artifactIds);

        // Step - Create project with document
        JSONObject docCreated = createOrUpdateDocumentJson(projectVersion, documentJson);

        // Step - Get list of artifact positions
        List<LayoutPosition> artifactPositions = getArtifactPositionsInDocument(
            projectCommit,
            docCreated,
            List.of(a1Name, a2Name, a3Name));

        // Step - Extract individual positions
        LayoutPosition a1Pos = artifactPositions.get(0);
        LayoutPosition a2Pos = artifactPositions.get(1);
        LayoutPosition a3Pos = artifactPositions.get(2);

        // VP - Verify that layout is correct
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }
}
