package edu.nd.crc.safa.test.features.attributes.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.features.attributes.AttributesForTesting;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestAttributeValueCrud extends AbstractCrudTest<ArtifactAppEntity> {

    private final AttributesForTesting attributesForTesting = new AttributesForTesting();
    @Autowired
    AttributeSystemServiceProvider attributeServiceProvider;
    private CustomAttributeType currentType;
    private CustomAttribute currentAttribute;
    private UUID currentId;

    @Override
    @Test
    public void testCrud() throws Exception {
        for (CustomAttributeType attributeType : CustomAttributeType.values()) {
            currentType = attributeType;
            super.testCrud();
            this.rootBuilder.clear();
        }
    }

    @Override
    protected List<String> getTopic() {
        String topic = TopicCreator.getVersionTopic(projectVersion.getVersionId());
        return List.of(topic);
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

        ProjectCommitDefinition commit = commitService
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
    protected void verifyCreationMessages(List<EntityChangeMessage> creationMessages) {
        assertThat(creationMessages).hasSize(1);
        changeMessageVerifies.verifyArtifactMessage(creationMessages.get(0), currentId, NotificationAction.UPDATE);
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
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        changeMessageVerifies.verifyArtifactMessage(updateMessages.get(0), currentId, NotificationAction.UPDATE);
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
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(1);
        changeMessageVerifies.verifyArtifactMessage(deletionMessages.get(0), currentId, NotificationAction.DELETE);
    }
}
