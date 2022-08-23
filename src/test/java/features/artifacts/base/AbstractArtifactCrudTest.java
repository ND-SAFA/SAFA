package features.artifacts.base;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import builders.CommitBuilder;
import common.AbstractCrudTest;

public abstract class AbstractArtifactCrudTest extends AbstractCrudTest<ArtifactAppEntity> {
    ArtifactAppEntity artifact = getStartingArtifact();

    @Override
    protected UUID getTopicId() {
        return this.projectVersion.getVersionId();
    }

    @Override
    protected IAppEntityService<ArtifactAppEntity> getAppService() {
        return this.serviceProvider.getArtifactService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        ProjectCommit commit = commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withAddedArtifact(artifact));

        String artifactId = commit.getArtifact(ModificationType.ADDED, 0).getId();
        artifact.setId(artifactId);
        return UUID.fromString(artifactId);
    }

    @Override
    protected void verifyCreatedEntity(ArtifactAppEntity retrievedEntity) {
        assertionService.assertMatch(artifact, retrievedEntity);
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyArtifactMessage(creationMessage, Change.Action.UPDATE, true);
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
        verifyArtifactMessage(updateMessage, Change.Action.UPDATE, false);
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
        verifyArtifactMessage(deletionMessage, Change.Action.DELETE, true);
    }

    private void verifyArtifactMessage(EntityChangeMessage message,
                                       Change.Action action,
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
