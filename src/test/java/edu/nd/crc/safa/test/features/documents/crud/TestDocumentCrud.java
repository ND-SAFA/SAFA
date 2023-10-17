package edu.nd.crc.safa.test.features.documents.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that a document can be created, retreived, updated, and deleted.
 */
public class TestDocumentCrud extends AbstractCrudTest<DocumentAppEntity> {
    String newName = "new-name";
    DocumentAppEntity document = new DocumentAppEntity(
        null,
        "document-name",
        "document-description",
        new ArrayList<>(),
        new HashMap<>()
    );

    @Override
    protected void onPostSubscribe() throws Exception {
        this.rootBuilder
            .notifications(n -> n.getEntityMessage(getCurrentUser()))
            .consume(m -> this.rootBuilder
                .verify(v -> v
                    .notifications(n -> n.verifyMemberNotification(m, List.of(currentUserName)))));
    }

    @Override
    protected List<String> getTopic() {
        String projectTopic = TopicCreator.getProjectTopic(this.project.getProjectId());
        String versionTopic = TopicCreator.getVersionTopic(this.projectVersion.getVersionId());
        return List.of(projectTopic, versionTopic);
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
    protected void verifyCreationMessages(List<EntityChangeMessage> creationMessages) {
        assertThat(creationMessages).hasSize(1);
        EntityChangeMessage creationMessage = creationMessages.get(0);
        messageVerificationService.verifyDocumentChange(
            creationMessage,
            entityId,
            NotificationAction.UPDATE);
        messageVerificationService.verifyUpdateLayout(creationMessage, false);
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
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        EntityChangeMessage updateMessage = updateMessages.get(0);
        messageVerificationService.verifyDocumentChange(
            updateMessage,
            entityId,
            NotificationAction.UPDATE);
        messageVerificationService.verifyUpdateLayout(updateMessage, false);
    }

    @Override
    protected void deleteEntity(DocumentAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
            .withDocument(document)
            .deleteWithJsonObject();
    }

    @Override
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(1);
        EntityChangeMessage deletionMessage = deletionMessages.get(0);
        messageVerificationService.verifyDocumentChange(
            deletionMessage,
            entityId,
            NotificationAction.DELETE);
        messageVerificationService.verifyUpdateLayout(deletionMessage, false);

    }
}
