package edu.nd.crc.safa.features.models.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.entities.ModelProject;
import edu.nd.crc.safa.features.models.repositories.ModelProjectRepository;
import edu.nd.crc.safa.features.models.repositories.ModelRepository;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides API for performing CRUD operations on models.
 */
@AllArgsConstructor
@Service
public class ModelService implements IAppEntityService<ModelAppEntity> {

    private final ModelProjectRepository modelProjectRepository;
    private final ModelRepository modelRepository;
    private final ProjectService projectService;

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
    public ModelAppEntity createOrUpdateModel(Project project, ModelAppEntity modelAppEntity) {
        // Step - Create model
        Model model = new Model(modelAppEntity);
        this.modelRepository.save(model);
        modelAppEntity.setId(model.getId());

        // Step - Create link between model and project
        Optional<ModelProject> modelProjectOptional = this.modelProjectRepository.findByModelAndProject(model, project);
        if (modelProjectOptional.isEmpty()) {
            ModelProject modelProject = new ModelProject(model, project);
            this.modelProjectRepository.save(modelProject);
        }

        return modelAppEntity;
    }

    /**
     * Returns list of models user has access to.
     *
     * @param user the user accessing the models
     * @return The list of models.
     */
    public List<ModelAppEntity> getUserModels(SafaUser user) {
        List<String> projectIds = this.projectService
            .getProjectsForUser(user)
            .stream()
            .map(ProjectIdAppEntity::getProjectId)
            .collect(Collectors.toList());

        HashMap<UUID, Model> modelProjectHashMap = new HashMap<>();
        List<ModelAppEntity> userModels = new ArrayList<>();

        this.modelProjectRepository
            .getAllModels()
            .stream()
            .filter(mp -> projectIds.contains(mp.getProject().getProjectId().toString()))
            .forEach(mp -> {
                Model model = mp.getModel();
                if (!modelProjectHashMap.containsKey(model.getId())) {
                    modelProjectHashMap.put(mp.getModel().getId(), mp.getModel());
                    userModels.add(new ModelAppEntity(model));
                }
            });
        return userModels;
    }

    @Override
    public List<ModelAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return getUserModels(user);
    }
}
