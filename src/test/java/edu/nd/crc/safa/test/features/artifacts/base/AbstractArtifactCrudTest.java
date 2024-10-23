package edu.nd.crc.safa.test.features.artifacts.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.services.CommonRequestService;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

public abstract class AbstractArtifactCrudTest extends AbstractCrudTest<ArtifactAppEntity> {
    ArtifactAppEntity artifact = getStartingArtifact();

    @Override
    protected List<String> getTopic() {
        String topic = TopicCreator.getVersionTopic(this.projectVersion.getVersionId());
        return List.of(topic);
    }

    @Override
    protected IAppEntityService<ArtifactAppEntity> getAppService() {
        return this.serviceProvider.getArtifactService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        this.rootBuilder.request(CommonRequestService::project);

        ProjectCommitDefinition commit = commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withAddedArtifact(artifact));

        UUID artifactId = commit.getArtifact(ModificationType.ADDED, 0).getId();
        artifact.setId(artifactId);
        return artifactId;
    }

    @Override
    protected void verifyCreatedEntity(ArtifactAppEntity retrievedEntity) {
        assertionService.assertMatch(artifact, retrievedEntity);
    }

    @Override
    protected void verifyCreationMessages(List<EntityChangeMessage> creationMessages) {
        assertThat(creationMessages).hasSize(2);
        EntityChangeMessage typeCreationMessage = creationMessages.get(0);
        rootBuilder.verify(v -> v.notifications(n -> n
            .verifyArtifactTypeMessage(typeCreationMessage, artifact.getType())));
        EntityChangeMessage artifactCreationMessage = creationMessages.get(1);
        verifyArtifactMessage(artifactCreationMessage, NotificationAction.UPDATE, true);
    }

    @Override
    protected void updateEntity() throws Exception {
        this.modifyArtifact(artifact);
        commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withModifiedArtifact(artifact));
    }

    @Override
    protected void verifyUpdatedEntity(ArtifactAppEntity retrievedEntity) {
        assertionService.assertMatch(artifact, retrievedEntity);
    }

    @Override
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        verifyArtifactMessage(updateMessages.get(0), NotificationAction.UPDATE, false);
    }

    @Override
    protected void deleteEntity(ArtifactAppEntity entity) {
        commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedArtifact(artifact));
    }

    @Override
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(2);
        EntityChangeMessage typeUpdateMessage = deletionMessages.get(0);
        this.rootBuilder.verify(v -> v.notifications(n -> n
            .verifyArtifactTypeMessage(typeUpdateMessage, artifact.getType())));
        EntityChangeMessage deletionMessage = deletionMessages.get(1);
        verifyArtifactMessage(deletionMessage, NotificationAction.DELETE, true);
    }

    private void verifyArtifactMessage(EntityChangeMessage message,
                                       NotificationAction action,
                                       boolean updateLayout) {
        this.messageVerificationService.verifyArtifactMessage(message, entityId, action);
        this.messageVerificationService.verifyWarningMessage(message);
        this.messageVerificationService.verifyUpdateLayout(message, updateLayout);
    }

    /**
     * @return {@link ArtifactAppEntity} Artifact to create and test.
     */
    protected abstract ArtifactAppEntity getStartingArtifact();

    /**
     * Performs a modification on artifact
     */
    protected abstract void modifyArtifact(ArtifactAppEntity artifact);
}
