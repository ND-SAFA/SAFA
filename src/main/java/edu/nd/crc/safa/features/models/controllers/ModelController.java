package edu.nd.crc.safa.features.models.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.tgen.method.bert.TBert;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
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
    public ModelAppEntity createModel(@PathVariable UUID projectId,
                                      @RequestBody ModelAppEntity modelAppEntity) {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        if (modelAppEntity.getId() != null) {
            throw new IllegalArgumentException("Model cannot be updated. Please delete and create new one.");
        }

        // Step - Create path for model state
        modelAppEntity = this.serviceProvider.getModelService().createModel(project, modelAppEntity);

        // Step - Copy model to project
        TBert bertModel = this.serviceProvider.getBertService().getBertModel(
            modelAppEntity.getBaseModel(),
            serviceProvider.getSafaRequestBuilder()
        );
        bertModel.createModel(modelAppEntity.getStatePath());

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
        this.serviceProvider.getModelRepository().delete(model);

        this.serviceProvider.getModelProjectRepository().findByModel(model).forEach((mp) -> {
            this.serviceProvider.getNotificationService().broadcastChange(
                EntityChangeBuilder
                    .create(mp.getProject())
                    .withModelDelete(modelId)
            );
        });
    }
}
