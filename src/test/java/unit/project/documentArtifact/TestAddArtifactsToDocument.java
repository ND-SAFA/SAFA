package unit.project.documentArtifact;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Tests that the client is able to add multiple artifact to some
 * specified document.
 */
class TestAddArtifactsToDocument extends ApplicationBaseTest {

    @Autowired
    DocumentArtifactRepository documentArtifactRepository;

    /**
     * Verifies that the response object contains
     */
    @Test
    void testCreateNewDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docDescription = "this is a description";
        DocumentType docType = DocumentType.ARTIFACT_TREE;

        String artifactType = "requirement";
        String artifactName = "RE-10";
        String artifactSummary = "summary";
        String artifactContent = "content";

        // Step - Create empty project with empty document and a three artifact
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactType)
            .newArtifactAndBody(projectName,
                artifactType, artifactName, artifactSummary, artifactContent)
            .newDocument(projectName, docName, docDescription, docType)
            .getProjectVersion(projectName, 0);
        Document document = dbEntityBuilder.getDocument(projectName, docName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        // Step - Create request payload
        JSONObject artifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifactAndReturn(projectName, artifact.getArtifactId().toString(),
                artifactName, artifactType,
                artifactContent);
        JSONArray artifactsJson = new JSONArray();
        artifactsJson.put(artifactJson);

        // Step - Request artifact is added to document

        JSONArray artifactsAdded = addArtifactToDocument(projectVersion, document, artifactsJson);

        // VP - Verify that response object contains name, description, and type
        for (int i = 0; i < artifactsAdded.length(); i++) {
            JSONObject artifactAdded = artifactsAdded.getJSONObject(i);
            JSONArray artifactDocuments = artifactAdded.getJSONArray("documentIds");
            assertThat(artifactDocuments.length()).isEqualTo(1);
            assertThat(artifactDocuments.get(0)).isEqualTo(document.getDocumentId().toString());
        }

        // VP - Verify single document created for project
        List<DocumentArtifact> projectDocuments = this.documentArtifactRepository.findByDocument(document);
        assertThat(projectDocuments.size()).isEqualTo(1);
    }
}
