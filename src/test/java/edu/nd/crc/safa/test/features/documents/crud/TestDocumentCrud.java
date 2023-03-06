package edu.nd.crc.safa.test.features.documents.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that a document can be created, retreived, updated, and deleted.
 */
public class TestDocumentCrud extends AbstractCrudTest<DocumentAppEntity> {
    String newName = "new-name";
    DocumentAppEntity document = new DocumentAppEntity(
        null,
        DocumentType.ARTIFACT_TREE,
        "document-name",
        "document-description",
        new ArrayList<>(),
        new ArrayList<>(),
        new HashMap<>()
    );

    @Override
    protected UUID getTopicId() {
        return this.project.getProjectId();
    }

    @Override
    protected IAppEntityService<DocumentAppEntity> getAppService() {
        return this.serviceProvider.getDocumentService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        creationService.createOrUpdateDocument(projectVersion, document);
        return document.getDocumentId();
    }

    @Override
    protected void verifyCreatedEntity(DocumentAppEntity retrievedEntity) {
        this.assertionService.assertMatch(document, retrievedEntity);
        this.layoutTestService.verifyLayout(retrievedEntity.getLayout(), retrievedEntity.getArtifactIds());
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        changeMessageVerifies.verifyDocumentChange(
            creationMessage,
            entityId,
            Change.Action.UPDATE);
        changeMessageVerifies.verifyUpdateLayout(creationMessage, false);
    }

    @Override
    protected void updateEntity() throws Exception {
        document.setName(newName);
        SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(document);
    }

    @Override
    protected void verifyUpdatedEntity(DocumentAppEntity retrievedEntity) {
        assertionService.assertMatch(document, retrievedEntity);
        assertThat(retrievedEntity.getName()).isEqualTo(newName);
        this.layoutTestService.verifyLayout(retrievedEntity.getLayout(), retrievedEntity.getArtifactIds());
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        changeMessageVerifies.verifyDocumentChange(
            updateMessage,
            entityId,
            Change.Action.UPDATE);
        changeMessageVerifies.verifyUpdateLayout(updateMessage, false);
    }

    @Override
    protected void deleteEntity(DocumentAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
            .withDocument(document)
            .deleteWithJsonObject();
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        changeMessageVerifies.verifyDocumentChange(
            deletionMessage,
            entityId,
            Change.Action.DELETE);
        changeMessageVerifies.verifyUpdateLayout(deletionMessage, false);

    }
}
