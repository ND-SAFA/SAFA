package features.layout.crud;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import features.layout.base.AbstractCorrectnessTest;
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
        ProjectCommit commit = createProject();
        Document document = this.dbEntityBuilder
            .newDocument(projectName, documentName, "", DocumentType.ARTIFACT_TREE)
            .getDocument(projectName, documentName);

        // Step - Add artifacts to layout
        creationService.addArtifactToDocument(projectVersion, document, commit.getArtifacts().getAdded());

        // Step - Retrieve project (including layout)
        ProjectAppEntity project = retrievalService.getProjectAtVersion(projectVersion);

        // Step - Extract artifact positions
        String documentId = document.getDocumentId().toString();
        LayoutPosition a1Pos = getLayoutPositionInDocument(project, documentId, a1Name);
        LayoutPosition a2Pos = getLayoutPositionInDocument(project, documentId, a2Name);
        LayoutPosition a3Pos = getLayoutPositionInDocument(project, documentId, a3Name);

        // VP - Verify that root has greatest y
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }

    @Test
    void testDocumentLayoutOnCreation() throws Exception {
        String docName = "doc-name";
        DocumentType docType = DocumentType.ARTIFACT_TREE;
        String docDescription = "";

        // Step - Create project
        ProjectCommit projectCommit = createProject();
        List<String> artifactIds = projectCommit
            .getArtifacts()
            .getAdded()
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());

        // Step - Create new document payload
        JSONObject documentJson = jsonBuilder.createDocument(
            docName,
            docDescription,
            docType,
            artifactIds);

        // Step - Create project with document
        JSONObject docCreated = creationService.createOrUpdateDocumentJson(projectVersion, documentJson);

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
