package features.types;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.types.TypeAppEntity;
import edu.nd.crc.safa.features.types.TypeService;

import common.AbstractCrudTest;
import org.json.JSONObject;
import requests.SafaRequest;

public class TestArtifactTypeCrud extends AbstractCrudTest<TypeAppEntity> {
    String editTypePath = AppRoutes.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE;
    ArtifactType artifactType = new ArtifactType(project, Constants.name);

    protected UUID createEntity() throws Exception {
        JSONObject createdType = SafaRequest
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(artifactType);
        UUID typeId = UUID.fromString(createdType.getString("typeId"));
        artifactType.setTypeId(typeId);
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
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(artifactType);
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
