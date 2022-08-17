package features.types;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.types.TypeAppEntity;
import edu.nd.crc.safa.features.types.TypeService;

import common.AbstractCrudTest;
import org.json.JSONObject;

public class TestArifactTypeCrud extends AbstractCrudTest<TypeAppEntity> {
    String editTypePath = AppRoutes.ArtifactType.CREATE_OR_UPDATE_ARTIFACT_TYPE;

    protected UUID createEntity() throws Exception {
        ArtifactType initialArtifactType = new ArtifactType(project, Constants.name);
        JSONObject createdType = SafaRequest
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(initialArtifactType);
        return UUID.fromString(createdType.getString("typeId"));
    }

    protected void verifyCreatedEntity(TypeAppEntity createdEntity) {
        assertThat(createdEntity.getName()).isEqualTo(Constants.name);
        assertThat(createdEntity.getIcon()).isNotNull();
    }

    protected void verifyCreationMessage(EntityChangeMessage message) {
        verifyUpdateMessage(message);
    }

    protected void updateEntity(TypeAppEntity updatedEntity) throws Exception {
        updatedEntity.setIcon(Constants.newIconName);
        SafaRequest
            .withRoute(editTypePath)
            .withProject(project)
            .postWithJsonObject(updatedEntity);
    }

    protected void verifyUpdatedEntity(TypeAppEntity updatedEntity) {
        assertThat(updatedEntity.getIcon()).isEqualTo(Constants.newIconName);
    }

    protected void verifyUpdateMessage(EntityChangeMessage message) {
        assertThat(message.getChanges()).hasSize(1);
        assertionTestService.verifyChangeInMessage(message,
            entityId,
            Change.Entity.TYPES,
            Change.Action.UPDATE);
    }

    protected void deleteEntity(TypeAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.ArtifactType.DELETE_ARTIFACT_TYPE)
            .withType(entity)
            .deleteWithJsonObject();
    }

    protected void verifyDeletionMessage(EntityChangeMessage message) {
        assertThat(message.getChanges()).hasSize(1);
        assertionTestService.verifyChangeInMessage(message,
            entityId,
            Change.Entity.TYPES,
            Change.Action.DELETE);
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
