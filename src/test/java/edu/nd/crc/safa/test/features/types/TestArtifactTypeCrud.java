package edu.nd.crc.safa.test.features.types;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;

public class TestArtifactTypeCrud extends AbstractCrudTest<TypeAppEntity> {
    ArtifactType artifactType = new ArtifactType(project, Constants.name, "");

    protected UUID createEntity() throws Exception {
        JSONObject createdType = SafaRequest
            .withRoute(AppRoutes.ArtifactType.CREATE_ARTIFACT_TYPE)
            .withProject(project)
            .postWithJsonObject(artifactType);
        UUID typeId = UUID.fromString(createdType.getString("typeId"));
        artifactType.setId(typeId);
        return typeId;
    }

    protected void verifyCreatedEntity(TypeAppEntity retrievedEntity) {
        assertThat(retrievedEntity.getName()).isEqualTo(Constants.name);
        assertThat(retrievedEntity.getIcon()).isNotNull();
    }

    protected void verifyCreationMessages(List<EntityChangeMessage> messages) {
        verifyUpdateMessages(messages);
    }

    protected void updateEntity() throws Exception {
        artifactType.setIcon(Constants.newIconName);
        SafaRequest
            .withRoute(AppRoutes.ArtifactType.UPDATE_ARTIFACT_TYPE)
            .withProject(project)
            .withArtifactType(artifactType.getName())
            .putWithJsonObject(artifactType);
    }

    protected void verifyUpdatedEntity(TypeAppEntity retrievedEntity) {
        assertThat(retrievedEntity.getIcon()).isEqualTo(Constants.newIconName);
    }

    protected void verifyUpdateMessages(List<EntityChangeMessage> messages) {
        EntityChangeMessage message = messages.get(0);
        assertThat(message.getChanges()).hasSize(1);
        this.messageVerificationService.verifyTypeChange(message,
            entityId,
            NotificationAction.UPDATE);
        this.messageVerificationService.verifyUpdateLayout(message, false);
    }

    protected void deleteEntity(TypeAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
            .withType(entity)
            .deleteWithJsonObject();
    }

    protected void verifyDeletionMessages(List<EntityChangeMessage> messages) {
        assertThat(messages).hasSize(1);
        EntityChangeMessage message = messages.get(0);
        assertThat(message.getChanges()).hasSize(1);
        this.messageVerificationService.verifyTypeChange(message,
            entityId,
            NotificationAction.DELETE);
        this.messageVerificationService.verifyUpdateLayout(message, true);
    }

    @Override
    protected void onPostSubscribe() throws Exception {
        this.rootBuilder
            .notifications(n -> n.getEntityMessage(getCurrentUser())).save("root-project-members")
            .and()
            .verify((s, v) -> v.notifications(n -> n.verifyMemberNotification(s.getMessage("root-project-members"),
                List.of(currentUserName))));
    }

    @Override
    protected List<String> getTopic() {
        String topic = TopicCreator.getProjectTopic(this.project.getProjectId());
        return List.of(topic);
    }

    protected TypeService getAppService() {
        return this.serviceProvider.getTypeService();
    }

    static class Constants {
        public static final String name = "requirement";
        public static final String newIconName = "mdi-something-else";
    }
}
