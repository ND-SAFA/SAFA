package edu.nd.crc.safa.features.models.entities;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.generation.tgen.entities.BaseGenerationModels;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The model to create for project.
 */
@AllArgsConstructor
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

    public ModelAppEntity(BaseGenerationModels model) {
        this.id = model.getId();
        this.name = model.getName();
        this.baseModel = model;
    }

    /**
     * @param baseGenerationModel The base model whose state is returned.
     * @return Returns the state of the associated model
     */
    public static String getStatePath(BaseGenerationModels baseGenerationModel) {
        return baseGenerationModel.getStatePath();
    }

    /**
     * @return Returns the state path associated with base model.
     */
    public String getStatePath() {
        return ModelAppEntity.getStatePath(this.baseModel);
    }
}
