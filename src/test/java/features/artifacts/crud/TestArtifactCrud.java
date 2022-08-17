package features.artifacts.crud;

import java.util.HashMap;
import java.util.UUID;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import common.AbstractCrudTest;

public class TestArtifactCrud extends AbstractCrudTest<ArtifactAppEntity> {
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
        String id = commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withAddedArtifact(constants.artifact))
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
        constants.artifact.setSummary(Constants.updatedSummary);
        commitTestService.commit(CommitBuilder.withVersion(projectVersion).withModifiedArtifact(constants.artifact));
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

    class Constants {
        static final String updatedSummary = "new summary";
        final ArtifactAppEntity artifact = new ArtifactAppEntity("",
            "RE-20",
            "Requirements",
            "summary",
            "body",
            DocumentType.ARTIFACT_TREE,
            new HashMap<>()
        );
    }
}
