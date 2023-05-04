package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TracingRequest {
    /**
     * The method to generate trace links with.
     */
    @NotNull
    BaseGenerationModels method;
    /**
     * The model to use to generate trace links.
     */
    ModelAppEntity model;
    /**
     * List of artifact levels to trace.
     */
    List<ArtifactLevelRequest> artifactLevels;
}
