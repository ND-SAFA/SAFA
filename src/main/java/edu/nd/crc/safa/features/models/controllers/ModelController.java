package edu.nd.crc.safa.features.models.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.entities.ShareMethod;
import edu.nd.crc.safa.features.models.entities.api.ShareModelRequest;
import edu.nd.crc.safa.features.models.tgen.method.bert.TBert;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for performing CRUD operations on models
 */
@RestController
public class ModelController extends BaseController {
    public ModelController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Returns all model in project specified with id.
     *
     * @param projectId - The id of the project whose models are returned.
     * @return List of models created for project.
     */
    @GetMapping(AppRoutes.Models.MODEL_ROOT)
    public List<ModelAppEntity> getProjectModels(@PathVariable UUID projectId) {
        //TODO: Remove project id from this root.
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.serviceProvider.getModelService().getUserModels();
    }

    /**
     * Creates model given model by copying the base model into the project storage.
     *
     * @param projectId      The project to create the project under,
     * @param modelAppEntity The model to create or update.
     * @return {@link ModelAppEntity} The model created.
     */
    @PostMapping(AppRoutes.Models.MODEL_ROOT)
    public ModelAppEntity createOrUpdateModel(@PathVariable UUID projectId,
                                              @RequestBody ModelAppEntity modelAppEntity) {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        boolean createModel = modelAppEntity.getId() == null;
        // Step - Create path for model state
        modelAppEntity = this.serviceProvider.getModelService().createOrUpdateModel(project, modelAppEntity);

        // Step - Copy model to project
        if (createModel) {
            try {
                TBert bertModel = this.serviceProvider.getBertService().getBertModel(
                    modelAppEntity.getBaseModel(),
                    serviceProvider.getSafaRequestBuilder()
                );

                bertModel.createModel(modelAppEntity.getStatePath());
            } catch (Exception e) {
                Model model = this.serviceProvider.getModelService().getModelById(modelAppEntity.getId());
                this.serviceProvider.getModelRepository().delete(model);
                e.printStackTrace();
                throw new SafaError("Failed to create model.", e);
            }
        }

        // Step - Notify project users of new model
        this.serviceProvider.getNotificationService().broadcastChange(
            EntityChangeBuilder
                .create(project)
                .withModelUpdate(modelAppEntity.getId())
        );

        return modelAppEntity;
    }

    /**
     * Deletes the model with given id. 4XX is returned if error occurs while finding model
     *
     * @param modelId The id of the model to delete.
     */
    @DeleteMapping(AppRoutes.Models.DELETE_MODEL_BY_ID)
    public void deleteModelById(@PathVariable UUID modelId) {
        Model model = this.serviceProvider.getModelService().getModelById(modelId);
        ModelAppEntity modelAppEntity = new ModelAppEntity(model);

        // Step - Delete model record
        this.serviceProvider.getModelRepository().delete(model);

        // Step - Delete model files
        TBert bertModel = this.serviceProvider.getBertService().getBertModel(
            modelAppEntity.getBaseModel(),
            serviceProvider.getSafaRequestBuilder()
        );
        bertModel.deleteModel();

        this.serviceProvider.getModelProjectRepository().findByModel(model).forEach(mp ->
            this.serviceProvider.getNotificationService().broadcastChange(
                EntityChangeBuilder
                    .create(mp.getProject())
                    .withModelDelete(modelId)
            ));
    }

    /**
     * Edits information about a model within a given project. Currently only edits to the
     * model name are supported. Edits to fields other than the model name will simply be
     * ignored.
     *
     * @param projectId The ID of the project the model to edit exists under
     * @param modelId The ID of the model to edit
     * @param modelAppEntity The model object with all the data to update
     * @return The newly updated model
     * @throws SafaError When an attempt is made to update a field that is not allowed to change
     */
    @PutMapping(AppRoutes.Models.MODEL_BY_ID)
    public ModelAppEntity editModelById(@PathVariable UUID projectId,
                              @PathVariable UUID modelId,
                              @RequestBody ModelAppEntity modelAppEntity) throws SafaError {

        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();

        // Get model object as it currently is in the database
        Model model = this.serviceProvider.getModelService().getModelById(modelId);
        ModelAppEntity currentModelEntity = new ModelAppEntity(model);

        // Make updates
        updateCurrentModelObject(currentModelEntity, modelAppEntity);

        // Save results to database and return
        return this.serviceProvider.getModelService().createOrUpdateModel(project, currentModelEntity);

    }

    /**
     * Modifies {@code currentModel} to contain updated fields from {@code updatedModel} while also checking that
     * no fields were updated that aren't allowed to be.
     *
     * @param currentModel The current version of the model as it exists in the database.
     * @param updatedModel The new version of the model with the user's edits.
     * @throws SafaError When an attempt is made to update a disallowed field.
     */
    private void updateCurrentModelObject(ModelAppEntity currentModel, ModelAppEntity updatedModel) throws SafaError {
        checkNoUpdate(currentModel.getId(), updatedModel.getId(), "id");
        checkNoUpdate(currentModel.getBaseModel(), updatedModel.getBaseModel(), "baseModel");

        // If we make it here, no disallowed fields were updated, so we can update the fields that are allowed
        if (updatedModel.getName() != null) {
            currentModel.setName(updatedModel.getName());
        }
    }

    /**
     * Checks that a field was not updated between {@code oldValue} and {@code newValue}.
     * A field is considered to not be updated if the old value and new value are equal, or
     * if the new value is not set at all. If the field is updated, an exception is thrown.
     * Otherwise, this function does nothing.
     *
     * @param oldValue The old value of the field.
     * @param newValue The new value of the field.
     * @param fieldName The name of the field we are checking (used for informational purposes in the exception).
     * @param <T> The type of the field.
     * @throws SafaError If the field was in fact updated.
     */
    private <T> void checkNoUpdate(T oldValue, T newValue, String fieldName) throws SafaError {
        if (newValue != null && !newValue.equals(oldValue)) {
            throw new SafaError("Attempt to edit disallowed field: " + fieldName
                    + " - '" + oldValue + "' -> '" + newValue + "'");
        }
    }

    /**
     * Shares a model with a given project. Copy can be by value or reference.
     * Copy by value directly copies the model to new the project.
     * Copy by reference only references model on the other project.
     *
     * @param shareModelRequest Request containing target project, model, and share method.
     */
    @PostMapping(AppRoutes.Models.SHARE_MODEL)
    public void shareModel(@RequestBody ShareModelRequest shareModelRequest) {
        Project project = this.resourceBuilder.fetchProject(shareModelRequest.getTargetProject()).withEditProject();
        ModelAppEntity modelAppEntity = shareModelRequest.getModel();
        ShareMethod shareMethod = shareModelRequest.getShareMethod();

        if (shareMethod.equals(ShareMethod.COPY_BY_VALUE)) {
            UUID sourceId = modelAppEntity.getId();

            // Step - Create model-project association for new project
            modelAppEntity.setId(null);
            this.serviceProvider.getModelService().createOrUpdateModel(project, modelAppEntity);
            UUID targetId = modelAppEntity.getId();

            // Step - Copy model to new project
            TBert bertModel = this.serviceProvider.getBertService().getBertModel(
                modelAppEntity.getBaseModel(),
                serviceProvider.getSafaRequestBuilder()
            );
            bertModel.copyModel(
                ModelAppEntity.getStatePath(sourceId),
                ModelAppEntity.getStatePath(targetId));
        } else if (shareMethod.equals(ShareMethod.COPY_BY_REFERENCE)) {
            this.serviceProvider.getModelService().createOrUpdateModel(project, shareModelRequest.getModel());
        }
    }
}
