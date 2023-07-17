package edu.nd.crc.safa.test.features.types;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
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

    protected void verifyCreationMessage(EntityChangeMessage message) {
        verifyUpdateMessage(message);
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

    protected void verifyUpdateMessage(EntityChangeMessage message) {
        assertThat(message.getChanges()).hasSize(1);
        this.changeMessageVerifies.verifyTypeChange(message,
            entityId,
            Change.Action.UPDATE);
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }

    protected void deleteEntity(TypeAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
            .withType(entity)
            .deleteWithJsonObject();
    }

    protected void verifyDeletionMessage(EntityChangeMessage message) {
        assertThat(message.getChanges()).hasSize(1);
        this.changeMessageVerifies.verifyTypeChange(message,
            entityId,
            Change.Action.DELETE);
        this.changeMessageVerifies.verifyUpdateLayout(message, true);
    }

    @Override
    protected UUID getTopicId() {
        return this.project.getProjectId();
    }

    protected TypeService getAppService() {
        return this.serviceProvider.getTypeService();
    }

    static class Constants {
        public static final String name = "requirement";
        public static final String newIconName = "mdi-something-else";
    }
}
