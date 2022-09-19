package edu.nd.crc.safa.features.models.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.repositories.ModelRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides API for performing CRUD operations on models.
 */
@AllArgsConstructor
@Service
public class ModelService implements IAppEntityService<ModelAppEntity> {

    private final ModelRepository modelRepository;

    /**
     * Queries database for model with given id and returns it if found. Otherwise, error is thrown.
     *
     * @param modelId - The id of the model to return.
     * @return {@link Model} The model to query for.
     */
    public Model getModelById(UUID modelId) {
        Optional<Model> modelOptional = modelRepository.findById(modelId);
        if (modelOptional.isPresent()) {
            return modelOptional.get();
        } else {
            throw new SafaError("Could not find model with id: [%s].", modelId);
        }
    }

    /**
     * Creates model under project.
     *
     * @param project        The project where the model will be accessible.
     * @param modelAppEntity The model to create.
     * @return Created {@link ModelAppEntity}.
     */
    public ModelAppEntity createModel(Project project, ModelAppEntity modelAppEntity) {
        Model model = new Model(modelAppEntity,
            project);
        this.modelRepository.save(model);
        modelAppEntity.setId(model.getId());
        return modelAppEntity;
    }

    /**
     * Updates given model app entity.
     *
     * @param modelAppEntity The model to update.
     * @return Updated {@link ModelAppEntity}.
     */
    public ModelAppEntity updateModel(ModelAppEntity modelAppEntity) {
        Model previousModel = getModelById(modelAppEntity.getId());
        Model model = new Model(modelAppEntity, previousModel.getProject());
        modelRepository.save(model);
        return modelAppEntity;
    }

    /**
     * Returns list of models under given project.
     *
     * @param project The project whose models are returned.
     * @return The list of models.
     */
    public List<ModelAppEntity> getProjectModels(Project project) {
        return this.modelRepository.
            findByProject(project)
            .stream()
            .map(ModelAppEntity::new)
            .collect(Collectors.toList());
    }

    @Override
    public List<ModelAppEntity> getAppEntities(ProjectVersion projectVersion) {
        return getProjectModels(projectVersion.getProject());
    }
}
