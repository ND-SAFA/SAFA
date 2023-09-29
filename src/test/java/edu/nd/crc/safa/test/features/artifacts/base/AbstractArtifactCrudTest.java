package edu.nd.crc.safa.test.features.artifacts.base;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.builders.CommitBuilder;
import edu.nd.crc.safa.test.common.AbstractCrudTest;

public abstract class AbstractArtifactCrudTest extends AbstractCrudTest<ArtifactAppEntity> {
    ArtifactAppEntity artifact = getStartingArtifact();

    @Override
    protected String getTopic() {
        return TopicCreator.getVersionTopic(this.projectVersion.getVersionId());
    }

    @Override
    protected IAppEntityService<ArtifactAppEntity> getAppService() {
        return this.serviceProvider.getArtifactService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        dbEntityBuilder.newCustomAttribute(projectName, CustomAttributeType.TEXT, "key", "key");

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
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyArtifactMessage(creationMessage, NotificationAction.UPDATE, true);
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
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        verifyArtifactMessage(updateMessage, NotificationAction.UPDATE, false);
    }

    @Override
    protected void deleteEntity(ArtifactAppEntity entity) throws Exception {
        commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedArtifact(artifact));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        verifyArtifactMessage(deletionMessage, NotificationAction.DELETE, true);
    }

    private void verifyArtifactMessage(EntityChangeMessage message,
                                       NotificationAction action,
                                       boolean updateLayout) {
        this.changeMessageVerifies.verifyArtifactMessage(message, entityId, action);
        this.changeMessageVerifies.verifyWarningMessage(message);
        this.changeMessageVerifies.verifyUpdateLayout(message, updateLayout);
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
