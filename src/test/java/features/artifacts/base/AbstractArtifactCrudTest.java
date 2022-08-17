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
    Constants constants = new Constants();

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
                .withAddedArtifact(constants.artifact));
        String id = commitJson
            .getJSONObject("artifacts")
            .getJSONArray("added")
            .getJSONObject(0)
            .getString("id");
        constants.artifact.setId(id);
        return UUID.fromString(id);
    }

    @Override
    protected void verifyCreatedEntity(ArtifactAppEntity createdEntity) {
        assertionTestService.assertMatch(constants.artifact, createdEntity);
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyArtifactMessage(creationMessage, Change.Action.UPDATE);
    }

    @Override
    protected void updateEntity(ArtifactAppEntity updatedEntity) throws Exception {
        this.modifyArtifact(constants.artifact);
        commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withModifiedArtifact(constants.artifact));
    }

    @Override
    protected void verifyUpdatedEntity(ArtifactAppEntity updatedEntity) {
        assertionTestService.assertMatch(constants.artifact, updatedEntity);
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
                .withRemovedArtifact(constants.artifact));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        verifyArtifactMessage(deletionMessage, Change.Action.DELETE);
    }

    private void verifyArtifactMessage(EntityChangeMessage message,
                                       Change.Action action) {
        assertionTestService.verifyChangeInMessage(message,
            entityId,
            Change.Entity.ARTIFACTS,
            action);
        assertionTestService.verifyChangeInMessage(message,
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

    protected class Constants {
        protected final ArtifactAppEntity artifact = getStartingArtifact();
    }
}
