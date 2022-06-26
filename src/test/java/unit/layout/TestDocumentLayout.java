package unit.layout;

import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentType;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that nodes are formatted in a hierarchical structure.
 */
public class TestDocumentLayout extends BaseCorrectnessTest {

    @Test
    public void testSimpleDocumentLayout() throws Exception {
        String documentName = "test-document";

        // Step - Create project
        JSONObject commitResponse = createProject();
        Document document = this.dbEntityBuilder
            .newDocument(projectName, documentName, "", DocumentType.ARTIFACT_TREE)
            .getDocument(projectName, documentName);

        // Step - Add artifacts to layout
        JSONArray artifactsJson = commitResponse.getJSONObject("artifacts").getJSONArray("added");
        addArtifactToDocument(projectVersion, document, artifactsJson);

        // Step - Create layout
        ProjectAppEntity project = getProjectAtVersion(projectVersion);

        // Step - Extract positions
        String documentId = document.getDocumentId().toString();
        LayoutPosition a1Pos = getPositionInDocument(project, documentId, a1Name);
        LayoutPosition a2Pos = getPositionInDocument(project, documentId, a2Name);
        LayoutPosition a3Pos = getPositionInDocument(project, documentId, a3Name);

        // VP - Verify that root has greatest y
        assertLayoutCorrectness(a1Pos, a2Pos, a3Pos);
    }
}
