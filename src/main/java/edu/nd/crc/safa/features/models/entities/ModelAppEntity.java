package edu.nd.crc.safa.features.models.entities;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The model to create for project.
 */
@NoArgsConstructor
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

    public ModelAppEntity(Model model) {
        this.id = model.getId();
        this.name = model.getName();
        this.baseModel = model.getBaseModel();
    }

    public static String getStatePath(UUID modelId) {
        return String.format("models/%s", modelId);
    }

    public String getStatePath() {
        return ModelAppEntity.getStatePath(this.id);
    }
}
