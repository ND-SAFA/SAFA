package edu.nd.crc.safa.test.features.attributes.crud;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributePositionAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestAttributeLayoutCrud extends AbstractCrudTest<AttributeLayoutAppEntity> {

    AttributeLayoutAppEntity attributeLayoutAppEntity = new AttributeLayoutAppEntity(
            null,
            "test layout",
            List.of("type1", "type2"),
            List.of(
                    new AttributePositionAppEntity("key1", 1, 2, 3, 4),
                    new AttributePositionAppEntity("key2", 5, 6, 7, 8)
            )
    );

    AttributeLayoutAppEntity updatedAttributeLayoutAppEntity = new AttributeLayoutAppEntity(
            null,
            "test layout - update",
            List.of("type3"),
            List.of(
                    new AttributePositionAppEntity("key3", 9, 10, 11, 12)
            )
    );

    @Override
    protected UUID getTopicId() {
        return project.getProjectId();
    }

    @Override
    protected IAppEntityService<AttributeLayoutAppEntity> getAppService() {
        return serviceProvider.getAttributeLayoutService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        dbEntityBuilder.newType(projectName, "type1")
                .newType(projectName, "type2")
                .newType(projectName, "type3")
                .newCustomAttribute(projectName, CustomAttributeType.BOOLEAN, "key1", "key1")
                .newCustomAttribute(projectName, CustomAttributeType.BOOLEAN, "key2", "key2")
                .newCustomAttribute(projectName, CustomAttributeType.BOOLEAN, "key3", "key3");

        JSONObject response = SafaRequest
                        .withRoute(AppRoutes.AttributeLayout.ROOT)
                        .withProject(project)
                        .postWithJsonObject(attributeLayoutAppEntity);

        return UUID.fromString(response.getString("id"));
    }

    @Override
    protected void verifyCreatedEntity(AttributeLayoutAppEntity retrievedEntity) {
        assertEquals(attributeLayoutAppEntity.getName(), retrievedEntity.getName());
        assertEquals(attributeLayoutAppEntity.getArtifactTypes(), retrievedEntity.getArtifactTypes());
        assertEquals(attributeLayoutAppEntity.getPositions(), retrievedEntity.getPositions());
        assertNotNull(retrievedEntity.getId());
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        changeMessageVerifies.verifyChangeInMessage(creationMessage, project.getProjectId(),
            Change.Entity.PROJECT, Change.Action.UPDATE);
    }

    @Override
    protected void updateEntity() throws Exception {
        SafaRequest
                .withRoute(AppRoutes.AttributeLayout.BY_ID)
                .withProject(project)
                .withId(entityId)
                .putWithJsonObject(updatedAttributeLayoutAppEntity);
    }

    @Override
    protected void verifyUpdatedEntity(AttributeLayoutAppEntity retrievedEntity) {
        assertEquals(updatedAttributeLayoutAppEntity.getName(), retrievedEntity.getName());
        assertEquals(updatedAttributeLayoutAppEntity.getArtifactTypes(), retrievedEntity.getArtifactTypes());
        assertEquals(updatedAttributeLayoutAppEntity.getPositions(), retrievedEntity.getPositions());
        assertNotNull(retrievedEntity.getId());
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        changeMessageVerifies.verifyChangeInMessage(updateMessage, project.getProjectId(),
            Change.Entity.PROJECT, Change.Action.UPDATE);
    }

    @Override
    protected void deleteEntity(AttributeLayoutAppEntity entity) throws Exception {
        SafaRequest
                .withRoute(AppRoutes.AttributeLayout.BY_ID)
                .withProject(project)
                .withId(entityId)
                .deleteWithJsonObject();
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        changeMessageVerifies.verifyChangeInMessage(deletionMessage, project.getProjectId(),
            Change.Entity.PROJECT, Change.Action.UPDATE);
    }

    @Test
    public void testGetLayout() throws Exception {
        project = dbEntityBuilder.newProjectWithReturn(projectName);
        UUID entityId = createEntity();

        AttributeLayoutAppEntity layoutEntity = SafaRequest
                .withRoute(AppRoutes.AttributeLayout.BY_ID)
                .withProject(project)
                .withId(entityId)
                .getAsType(new TypeReference<>() {});

        verifyCreatedEntity(layoutEntity);
    }

    @Test
    public void testGetAllLayouts() throws Exception {
        project = dbEntityBuilder.newProjectWithReturn(projectName);
        createEntity();

        List<AttributeLayoutAppEntity> layoutEntityList = SafaRequest
                .withRoute(AppRoutes.AttributeLayout.ROOT)
                .withProject(project)
                .getAsType(new TypeReference<>() {});

        assertEquals(1, layoutEntityList.size());
        verifyCreatedEntity(layoutEntityList.get(0));
    }
}
