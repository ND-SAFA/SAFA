package edu.nd.crc.safa.test.features.attributes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.DoubleNode;
import com.fasterxml.jackson.databind.node.IntNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.TextNode;
import org.junit.jupiter.api.Test;

public class TestAttributeValueCrud extends AbstractCrudTest<ArtifactAppEntity> {

    private final String artifactType = "Requirement";
    private final JsonNode updatedValue = TextNode.valueOf("thisissomenewvalue");
    private UUID currentId;
    private JsonNode currentValue;
    private String currentKey;

    @Override
    @Test
    public void testCrud() throws Exception {
        ArrayNode intArray = JsonNodeFactory.instance.arrayNode();
        intArray.add(1);
        intArray.add(2);

        ObjectNode objectKey = JsonNodeFactory.instance.objectNode();
        objectKey.put("some_key", "hi");

        Map<String, JsonNode> testValues = new HashMap<>();
        testValues.put("float_key", DoubleNode.valueOf(5.1F));
        testValues.put("int_key", IntNode.valueOf(5));
        testValues.put("str_key", TextNode.valueOf("5"));
        testValues.put("int_array", intArray);
        testValues.put("object_key", objectKey);

        for (Map.Entry<String, JsonNode> entry : testValues.entrySet()) {
            this.currentKey = entry.getKey();
            this.currentValue = entry.getValue();
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
        Map<String, JsonNode> customAttributes = new HashMap<>();
        customAttributes.put(currentKey, currentValue);
        ArtifactAppEntity artifact = new ArtifactAppEntity(null,
            artifactType,
            "RE-20",
            "summary",
            "body",
            customAttributes
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
        assertTrue(retrievedEntity.getAttributes().containsKey(currentKey));
        assertEquals(currentValue, retrievedEntity.getAttributes().get(currentKey));
    }

    @Override
    protected void verifyCreationMessages(List<EntityChangeMessage> creationMessages) {
        assertThat(creationMessages).hasSize(2);
        this.rootBuilder.verify(v -> v.notifications(n -> n
            .verifyArtifactTypeMessage(creationMessages.get(0), artifactType)));
        EntityChangeMessage artifactCreationMessage = creationMessages.get(1);
        messageVerificationService.verifyArtifactMessage(artifactCreationMessage, currentId, NotificationAction.UPDATE);
    }

    @Override
    protected void updateEntity() throws Exception {
        Map<String, JsonNode> customAttributes = new HashMap<>();
        customAttributes.put(currentKey, updatedValue);
        ArtifactAppEntity artifact = new ArtifactAppEntity(currentId,
            artifactType,
            "RE-20",
            "summary",
            "body",
            customAttributes
        );

        commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withModifiedArtifact(artifact));
    }

    @Override
    protected void verifyUpdatedEntity(ArtifactAppEntity retrievedEntity) {
        assertEquals(1, retrievedEntity.getAttributes().size());
        assertTrue(retrievedEntity.getAttributes().containsKey(currentKey));
        assertEquals(updatedValue, retrievedEntity.getAttributes().get(currentKey));
    }

    @Override
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        messageVerificationService.verifyArtifactMessage(updateMessages.get(0), currentId, NotificationAction.UPDATE);
    }

    @Override
    protected void deleteEntity(ArtifactAppEntity entity) throws Exception {
        Map<String, JsonNode> customAttributes = new HashMap<>();
        ArtifactAppEntity artifact = new ArtifactAppEntity(currentId,
            artifactType,
            "RE-20",
            "summary",
            "body",
            customAttributes
        );

        commitService.commit(CommitBuilder
            .withVersion(projectVersion)
            .withRemovedArtifact(artifact));
    }

    @Override
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(2);
        this.rootBuilder.verify(v -> v.notifications(n -> n
            .verifyArtifactTypeMessage(deletionMessages.get(0), artifactType)));
        messageVerificationService.verifyArtifactMessage(deletionMessages.get(1), currentId, NotificationAction.DELETE);
    }
}
