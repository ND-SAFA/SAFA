package edu.nd.crc.safa.test.features.attributes.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributePositionAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
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

    @Test
    void testGetAllLayouts() throws Exception {
        this.projectVersion = this.rootBuilder
            .actions(a -> a.createProjectWithVersion(currentUser)).get();
        this.project = this.projectVersion.getProject();

        this.rootBuilder
            .notifications((s, n) -> n
                .initializeUser(currentUser, this.token)
                .subscribeToProject(currentUser, this.project)
                .getEntityMessage(currentUser)).save("root-project-message")
            .and()
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("root-project-message"), List.of(currentUserName))));

        createEntity();

        List<AttributeLayoutAppEntity> layoutEntityList = SafaRequest
            .withRoute(AppRoutes.AttributeLayout.ROOT)
            .withProject(project)
            .getAsType(new TypeReference<>() {
            });

        assertEquals(1, layoutEntityList.size());
        verifyCreatedEntity(layoutEntityList.get(0));
    }

    @Override
    protected void onPostSubscribe() throws Exception {
        this.rootBuilder
            .notifications(n -> n.getEntityMessage(currentUser)).save("root-project-message")
            .and()
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("root-project-message"), List.of(currentUserName))));
    }

    @Override
    protected List<String> getTopic() {
        String topic = TopicCreator.getProjectTopic(project.getProjectId());
        return List.of(topic);
    }

    @Override
    protected IAppEntityService<AttributeLayoutAppEntity> getAppService() {
        return serviceProvider.getAttributeLayoutService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        this.rootBuilder
            .build((s, b) -> b
                .withType(this.project, t -> t.withName("type1").withDummyIcon().withColor("blue"))
                .withType(this.project, t -> t.withName("type2").withDummyIcon().withColor("red"))
                .withType(this.project, t -> t.withName("type3").withDummyIcon().withColor("green")))
            .and()
            .request((s, r) -> r.project()
                .createCustomAttribute("project", c -> c
                    .withType(CustomAttributeType.BOOLEAN)
                    .withLabel("key1")
                    .withKeyName("key1")
                    .withProject(project))
                .and()
                .createCustomAttribute("project", c -> c
                    .withType(CustomAttributeType.BOOLEAN)
                    .withLabel("key2")
                    .withKeyName("key2")
                    .withProject(project))
                .and()
                .createCustomAttribute("project", c -> c
                    .withType(CustomAttributeType.BOOLEAN)
                    .withLabel("key3")
                    .withKeyName("key3")
                    .withProject(project)));

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
    protected void verifyCreationMessages(List<EntityChangeMessage> messages) {
        this.verifyAttributeMessage(messages.get(0), NotificationAction.UPDATE);
        this.verifyAttributeMessage(messages.get(1), NotificationAction.UPDATE);
        this.verifyAttributeMessage(messages.get(2), NotificationAction.UPDATE);
        this.rootBuilder.verify(v -> v.notifications(n -> n.verifyProjectMessage(messages.get(3))));
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
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        EntityChangeMessage updateMessage = updateMessages.get(0);
        this.rootBuilder.verify(v -> v.notifications(n -> n.verifyMessage(updateMessage,
            List.of(NotificationEntity.PROJECT),
            List.of(NotificationAction.UPDATE),
            (i, e) -> assertThat(e).isEmpty())));
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
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(1);
        this.verifyAttributeMessage(deletionMessages.get(0), NotificationAction.DELETE);
    }

    @Test
    void testGetLayout() throws Exception {
        this.projectVersion = this.rootBuilder
            .build((s, b) -> b.project(currentUser).save("project"))
            .and()
            .build((s, b) -> b.version(v -> v.newVersion(s.getProject("project")))).get().get();
        this.project = this.projectVersion.getProject();
        this.rootBuilder
            .notifications((s, n) -> n
                .initializeUser(currentUser, this.token)
                .subscribeToProject(currentUser, s.getProject("project"))
                .getEntityMessage(currentUser))
            .consume(m -> this.rootBuilder
                .verify(v -> v.notifications(n -> n.verifyMemberNotification(m, List.of(currentUserName)))));

        UUID entityId = createEntity();

        AttributeLayoutAppEntity layoutEntity = SafaRequest
            .withRoute(AppRoutes.AttributeLayout.BY_ID)
            .withProject(project)
            .withId(entityId)
            .getAsType(new TypeReference<>() {
            });

        verifyCreatedEntity(layoutEntity);
    }

    private void verifyAttributeMessage(EntityChangeMessage message, NotificationAction action) {
        assertThat(message.getChanges()).hasSize(1);
        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(NotificationEntity.ATTRIBUTES);
        assertThat(change.getAction()).isEqualTo(action);
        //TODO: Check entity attributes
    }
}
