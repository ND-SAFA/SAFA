package edu.nd.crc.safa.features.models.entities;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;

import lombok.Data;

/**
 * The model to create for project.
 */

@Data
public class ModelAppEntity implements IAppEntity {

    /**
     * Unique identifier for model.
     */
    UUID id;

    /**
     * The client-side identifier for model.
     */
    String name;
    /**
     * The base model for generating trace links.
     */
    BaseGenerationModels baseModel;

    public ModelAppEntity(String name, BaseGenerationModels baseModel) {
        this.name = name;
        this.baseModel = baseModel;
    }

    public ModelAppEntity(Model model) {
        this.id = model.getId();
        this.name = model.getName();
        this.baseModel = model.getBaseModel();
    }

    public static String getStatePath(Project project, UUID modelId) {
        return String.format("projects/%s/models/%s", project.getProjectId(), modelId);
    }

    public String getStatePath(Project project) {
        return getStatePath(project, this.id);
    }
}
