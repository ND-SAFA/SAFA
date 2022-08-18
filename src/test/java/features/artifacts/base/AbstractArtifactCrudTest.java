package features.artifacts.base;

import java.util.UUID;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import common.AbstractCrudTest;
import org.json.JSONObject;

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
        JSONObject commitJson = commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withAddedArtifact(artifact));
        String id = commitJson
            .getJSONObject("artifacts")
            .getJSONArray("added")
            .getJSONObject(0)
            .getString("id");
        artifact.setId(id);
        return UUID.fromString(id);
    }

    @Override
    protected void verifyCreatedEntity(ArtifactAppEntity retrievedEntity) {
        assertionTestService.assertMatch(artifact, retrievedEntity);
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyArtifactMessage(creationMessage, Change.Action.UPDATE);
    }

    @Override
    protected void updateEntity() throws Exception {
        this.modifyArtifact(artifact);
        commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withModifiedArtifact(artifact));
    }

    @Override
    protected void verifyUpdatedEntity(ArtifactAppEntity retrievedEntity) {
        assertionTestService.assertMatch(artifact, retrievedEntity);
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        verifyArtifactMessage(updateMessage, Change.Action.UPDATE);
    }

    @Override
    protected void deleteEntity(ArtifactAppEntity entity) throws Exception {
        commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedArtifact(artifact));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        verifyArtifactMessage(deletionMessage, Change.Action.DELETE);
    }

    private void verifyArtifactMessage(EntityChangeMessage message,
                                       Change.Action action) {
        messageVerificationTestService.verifyArtifactMessage(message, entityId, action);
        messageVerificationTestService.verifyChangeInMessage(message,
            null,
            Change.Entity.WARNINGS,
            Change.Action.UPDATE);
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
