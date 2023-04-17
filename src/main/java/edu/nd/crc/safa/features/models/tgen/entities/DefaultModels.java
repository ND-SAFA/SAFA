package edu.nd.crc.safa.features.models.tgen.entities;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;

/**
 * Enumerates the default list of models available to all users.
 */
public class DefaultModels {
    /**
     * @return Returns list of models available to all useres.
     */
    public static List<ModelAppEntity> getDefaultModels() {
        return List.of(
            new ModelAppEntity(UUID.randomUUID(), "GPT", BaseGenerationModels.GPT)
        );
    }
}
