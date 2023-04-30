package edu.nd.crc.safa.features.models.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.entities.api.ShareModelRequest;
import edu.nd.crc.safa.features.models.tgen.entities.DefaultModels;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import org.apache.commons.lang3.NotImplementedException;
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
    @GetMapping(AppRoutes.Models.MODEL_ROOT_BY_ID)
    public List<ModelAppEntity> getProjectModels(@PathVariable UUID projectId) {
        this.resourceBuilder.fetchProject(projectId).withViewProject();
        return DefaultModels.getDefaultModels();
    }

    /**
     * Returns the list of registered models. No project is required.
     *
     * @return List of available models.
     */
    @GetMapping(AppRoutes.Models.MODEL_ROOT)
    public List<ModelAppEntity> getModels() {
        return DefaultModels.getDefaultModels();
    }

    /**
     * Creates model given model by copying the base model into the project storage.
     *
     * @param projectId      The project to create the project under,
     * @param modelAppEntity The model to create or update.
     * @return {@link ModelAppEntity} The model created.
     */
    @PostMapping(AppRoutes.Models.MODEL_ROOT_BY_ID)
    public ModelAppEntity createOrUpdateModel(@PathVariable UUID projectId,
                                              @RequestBody ModelAppEntity modelAppEntity) {
        throw new NotImplementedException("Creating or updating models has been deprecated. Please use default models"
            + " instead.");
    }

    /**
     * Deletes the model with given id. 4XX is returned if error occurs while finding model
     *
     * @param modelId The id of the model to delete.
     */
    @DeleteMapping(AppRoutes.Models.DELETE_MODEL_BY_ID)
    public void deleteModelById(@PathVariable UUID modelId) {
        throw new NotImplementedException("Deleting models has been deprecated. Please use default models instead.");
    }

    /**
     * Edits information about a model within a given project. Currently only edits to the
     * model name are supported. Edits to fields other than the model name will simply be
     * ignored.
     *
     * @param projectId      The ID of the project the model to edit exists under
     * @param modelId        The ID of the model to edit
     * @param modelAppEntity The model object with all the data to update
     * @return The newly updated model
     * @throws SafaError When an attempt is made to update a field that is not allowed to change
     */
    @PutMapping(AppRoutes.Models.MODEL_BY_PROJECT_AND_ID)
    public ModelAppEntity editModelById(@PathVariable UUID projectId,
                                        @PathVariable UUID modelId,
                                        @RequestBody ModelAppEntity modelAppEntity) throws SafaError {

        throw new NotImplementedException("Editing models has been deprecated. Please use default models instead.");
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
        throw new NotImplementedException("Sharing models has been deprecated. Please use default models instead.");
    }
}
