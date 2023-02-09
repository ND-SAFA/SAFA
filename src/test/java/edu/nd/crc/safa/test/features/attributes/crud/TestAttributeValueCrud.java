package edu.nd.crc.safa.test.features.attributes.crud;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.builders.CommitBuilder;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.features.attributes.AttributesForTesting;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestAttributeValueCrud extends AbstractCrudTest<ArtifactAppEntity> {

    @Autowired
    AttributeSystemServiceProvider attributeServiceProvider;

    private CustomAttributeType currentType;

    private CustomAttribute currentAttribute;

    private UUID currentId;

    private final AttributesForTesting attributesForTesting = new AttributesForTesting();

    @Override
    @Test
    public void testCrud() throws Exception {
        for (CustomAttributeType attributeType : CustomAttributeType.values()) {
            currentType = attributeType;
            super.testCrud();
        }
    }

    @Override
    protected UUID getTopicId() {
        return projectVersion.getVersionId();
    }

    @Override
    protected IAppEntityService<ArtifactAppEntity> getAppService() {
        return serviceProvider.getArtifactService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        currentAttribute = attributesForTesting.setupAttribute(dbEntityBuilder, projectName,
            attributeServiceProvider, currentType);

        ArtifactAppEntity artifact = new ArtifactAppEntity(null,
                "Requirements",
                "RE-20",
                "summary",
                "body",
                DocumentType.ARTIFACT_TREE,
                Map.of(currentAttribute.getKeyname(), attributesForTesting.attributes.get(currentType).value)
        );

        ProjectCommit commit = commitService
                .commit(CommitBuilder
                        .withVersion(projectVersion)
                        .withAddedArtifact(artifact));

        currentId = commit.getArtifact(ModificationType.ADDED, 0).getId();
        artifact.setId(currentId);
        return currentId;
    }

    @Override
    protected void verifyCreatedEntity(ArtifactAppEntity retrievedEntity) {
        assertEquals(1, retrievedEntity.getAttributes().size());
        assertTrue(retrievedEntity.getAttributes().containsKey(currentAttribute.getKeyname()));

        AttributesForTesting.AttributeInfo schemaInfo = attributesForTesting.attributes.get(currentAttribute.getType());
        assertEquals(schemaInfo.getValue(), retrievedEntity.getAttributes().get(currentAttribute.getKeyname()));
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        changeMessageVerifies.verifyArtifactMessage(creationMessage, currentId, Change.Action.UPDATE);
    }

    @Override
    protected void updateEntity() throws Exception {
        ArtifactAppEntity artifact = new ArtifactAppEntity(currentId,
                "Requirements",
                "RE-20",
                "summary",
                "body",
                DocumentType.ARTIFACT_TREE,
                Map.of(currentAttribute.getKeyname(), attributesForTesting.attributes.get(currentType).altValue)
        );

        commitService.commit(CommitBuilder
                        .withVersion(projectVersion)
                        .withModifiedArtifact(artifact));
    }

    @Override
    protected void verifyUpdatedEntity(ArtifactAppEntity retrievedEntity) {
        assertEquals(1, retrievedEntity.getAttributes().size());
        assertTrue(retrievedEntity.getAttributes().containsKey(currentAttribute.getKeyname()));

        AttributesForTesting.AttributeInfo schemaInfo = attributesForTesting.attributes.get(currentAttribute.getType());
        assertEquals(schemaInfo.getAltValue(), retrievedEntity.getAttributes().get(currentAttribute.getKeyname()));
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        changeMessageVerifies.verifyArtifactMessage(updateMessage, currentId, Change.Action.UPDATE);
    }

    @Override
    protected void deleteEntity(ArtifactAppEntity entity) throws Exception {
        ArtifactAppEntity artifact = new ArtifactAppEntity(currentId,
                "Requirements",
                "RE-20",
                "summary",
                "body",
                DocumentType.ARTIFACT_TREE,
                Map.of(currentAttribute.getKeyname(), attributesForTesting.attributes.get(currentType).altValue)
        );

        commitService.commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedArtifact(artifact));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        changeMessageVerifies.verifyArtifactMessage(deletionMessage, currentId, Change.Action.DELETE);
    }

}
