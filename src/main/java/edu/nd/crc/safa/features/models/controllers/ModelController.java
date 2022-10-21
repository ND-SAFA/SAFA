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
