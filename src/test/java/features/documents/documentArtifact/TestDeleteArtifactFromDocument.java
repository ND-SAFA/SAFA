package features.documents.documentArtifact;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.notifications.entities.old.VersionMessage;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is able to add multiple artifact to some
 * specified document.
 */
class TestDeleteArtifactFromDocument extends ApplicationBaseTest {

    @Autowired
    DocumentArtifactRepository documentArtifactRepository;

    /**
     * Verifies that the response object contains
     */
    @Test
    void testDeleteArtifactFromDocument() throws Exception {
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
            .newDocumentArtifact(projectName, 0, docName, artifactName)
            .getProjectVersion(projectName, 0);
        Document document = dbEntityBuilder.getDocument(projectName, docName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        // VP - Verify that artifact is linked
        Optional<DocumentArtifact> documentArtifactOptional =
            this.documentArtifactRepository.findByProjectVersionAndDocumentAndArtifact(projectVersion,
                document, artifact);
        assertThat(documentArtifactOptional).isPresent();

        // Step - Subscribe to version updates
        createNewConnection(defaultUser)
            .subscribeToVersion(defaultUser, projectVersion);

        // Step - Request artifact is removed from document
        String route = RouteBuilder.withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .withArtifactId(artifact)
            .buildEndpoint();
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Verify that artifact is no longer linked
        List<DocumentArtifact> documentArtifactList = this.documentArtifactRepository.findByDocument(document);
        assertThat(documentArtifactList).isEmpty();

        // VP - Verify that websocket message to update artifacts.
        VersionMessage message = getNextMessage(defaultUser, VersionMessage.class);
        assertThat(message.getType()).isEqualTo(VersionEntityTypes.ARTIFACTS);
    }
}
