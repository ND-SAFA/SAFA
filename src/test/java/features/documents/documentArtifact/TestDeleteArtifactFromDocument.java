package features.documents.documentArtifact;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

/**
 * Tests that the client is able to remove an artifact from a document
 */
class TestDeleteArtifactFromDocument extends ApplicationBaseTest {

    /**
     * Verifies that:
     * - Client is able to remove user from document
     * - Other members are notified that member has been removed.
     */
    @Test
    void testDeleteArtifactFromDocument() throws Exception {
        // Step - Create, project, document, three artifact
        ProjectVersion projectVersion = createProjectData();
        Document document = dbEntityBuilder.getDocument(projectName, DocumentConstants.name);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, ArtifactConstants.name);

        // VP - Verify that artifact is linked
        Optional<DocumentArtifact> documentArtifactOptional = this.documentArtifactRepository
            .findByProjectVersionAndDocumentAndArtifact(projectVersion, document, artifact);
        assertThat(documentArtifactOptional).isPresent();

        // Step - Subscribe to version updates as other member
        createNewConnection(defaultUser).subscribeToVersion(defaultUser, projectVersion);

        // Step - Request artifact is removed from document
        String route = RouteBuilder
            .withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .withArtifactId(artifact)
            .buildEndpoint();
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Verify that artifact is no longer linked
        List<DocumentArtifact> documentArtifactList = this.documentArtifactRepository.findByDocument(document);
        assertThat(documentArtifactList).isEmpty();

        // VP - Verify that 2 changes are detected (document + artifacts).
        EntityChangeMessage message = getNextMessage(defaultUser, EntityChangeMessage.class);
        assertThat(message.getChanges()).hasSize(2);

        // VP - Verify that change is for a deleted member
        List<Change.Entity> changedEntities =
            message.getChanges().stream().map(Change::getEntity).collect(Collectors.toList());
        Change change = message.getChanges().get(0);
        assertThat(changedEntities)
            .contains(Change.Entity.DOCUMENT)
            .contains(Change.Entity.ARTIFACTS);

        // VP - Verify document change has action: UPDATE
        Change documentChange = message.getChangeForEntity(Change.Entity.DOCUMENT);
        assertThat(documentChange.getAction()).isEqualTo(Change.Action.UPDATE);
        assertThat(documentChange.getEntityIds()).hasSize(1);

        // VP - Verify that artifact change has action: UPDATE
        Change artifactChange = message.getChangeForEntity(Change.Entity.ARTIFACTS);
        assertThat(artifactChange.getAction()).isEqualTo(Change.Action.UPDATE);
        assertThat(artifactChange.getEntityIds()).hasSize(1);
    }

    public ProjectVersion createProjectData() {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, ArtifactConstants.type)
            .newArtifactAndBody(projectName,
                ArtifactConstants.type,
                ArtifactConstants.name,
                ArtifactConstants.summary,
                ArtifactConstants.content)
            .newDocument(projectName,
                DocumentConstants.name,
                DocumentConstants.description,
                DocumentConstants.type)
            .newDocumentArtifact(projectName, 0, DocumentConstants.name, ArtifactConstants.name)
            .getProjectVersion(projectName, 0);
    }

    static class DocumentConstants {
        public static final String name = "test-document";
        public static final String description = "this is a description";
        public static final DocumentType type = DocumentType.ARTIFACT_TREE;
    }

    static class ArtifactConstants {
        public static final String name = "RE-10";
        public static final String summary = "summary";
        public static final String content = "content";
        public static final String type = "requirement";
    }
}
