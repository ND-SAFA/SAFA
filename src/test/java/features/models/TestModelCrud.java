package features.models;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;

import common.AbstractCrudTest;
import lombok.Data;
import requests.SafaRequest;

public class TestModelCrud extends AbstractCrudTest<ModelAppEntity> {

    private final String updatedModelName = "New project model";
    private final ModelAppEntity modelAppEntity = new ModelAppEntity(
        EntityConstants.name,
        EntityConstants.baseModel);

    @Override
    protected UUID getTopicId() {
        return this.project.getProjectId();
    }

    @Override
    protected IAppEntityService<ModelAppEntity> getAppService() {
        return this.serviceProvider.getModelService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        String modelIdStr = SafaRequest
            .withRoute(AppRoutes.Models.MODEL_ROOT)
            .withProject(project)
            .postWithJsonObject(modelAppEntity)
            .getString("id");
        UUID modelId = UUID.fromString(modelIdStr);
        modelAppEntity.setId(modelId);
        return modelId;
    }

    @Override
    protected void verifyCreatedEntity(ModelAppEntity retrievedEntity) {
        assertionService.assertMatch(modelAppEntity, retrievedEntity);
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyModelMessage(creationMessage, Change.Action.UPDATE);
    }

    @Override
    protected void updateEntity() throws Exception {
        modelAppEntity.setName(updatedModelName);
        SafaRequest
            .withRoute(AppRoutes.Models.MODEL_ROOT)
            .withProject(project)
            .postWithJsonObject(modelAppEntity);
    }

    @Override
    protected void verifyUpdatedEntity(ModelAppEntity retrievedEntity) {
        assertThat(retrievedEntity.getName()).isEqualTo(updatedModelName);
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        verifyModelMessage(updateMessage, Change.Action.UPDATE);
    }

    @Override
    protected void deleteEntity(ModelAppEntity entity) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Models.DELETE_MODEL_BY_ID)
            .withProject(project)
            .withModelId(modelAppEntity.getId())
            .deleteWithJsonObject();
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        verifyModelMessage(deletionMessage, Change.Action.DELETE);
    }

    private void verifyModelMessage(EntityChangeMessage message, Change.Action action) {
        this.changeMessageVerifies.verifyModelMessage(message, modelAppEntity.getId(), action);
    }

    @Data
    static class EntityConstants {
        static String name = "My project model.";
        static BaseGenerationModels baseModel = BaseGenerationModels.NLBert;
    }
}
