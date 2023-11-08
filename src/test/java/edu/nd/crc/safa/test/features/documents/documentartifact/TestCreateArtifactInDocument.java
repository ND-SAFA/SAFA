package edu.nd.crc.safa.test.features.documents.documentartifact;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is able to add multiple artifact to some
 * specified document.
 */
class TestCreateArtifactInDocument extends ApplicationBaseTest {

    @Autowired
    DocumentArtifactRepository documentArtifactRepository;

    /**
     * Verifies that the response object contains
     */
    @Test
    void testCreateArtifactInDocument() throws Exception {
        String projectName = "test-project";
        String docName = "test-document";
        String docDescription = "this is a description";

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
            .newDocument(projectName, docName, docDescription)
            .getProjectVersion(projectName, 0);
        Document document = dbEntityBuilder.getDocument(projectName, docName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        // Step - Create new document payload
        JSONObject artifactJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifactAndReturn(projectName, artifact.getArtifactId(),
                artifactName, artifactType,
                artifactContent);
        List<Object> documentIds = artifactJson.getJSONArray("documentIds").toList();
        documentIds.add(document.getDocumentId().toString());
        artifactJson.put("documentIds", documentIds);
        JSONArray requestPayload = new JSONArray();
        requestPayload.put(artifactJson);

        // Step -
        CommitBuilder commitBuilder = CommitBuilder.withVersion(projectVersion).withModifiedArtifact(artifactJson);
        commitService.commit(commitBuilder);

        // VP - Verify single document created for project
        List<DocumentArtifact> projectDocuments = this.documentArtifactRepository.findByDocument(document);
        assertThat(projectDocuments).hasSize(1);
    }
}
