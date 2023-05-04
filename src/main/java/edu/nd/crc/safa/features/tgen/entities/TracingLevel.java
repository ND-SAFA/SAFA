package edu.nd.crc.safa.features.tgen.entities;

import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class TracingLevel extends TracingRequest {
    /**
     * The method to generate trace links with.
     */
    @NotNull
    BaseGenerationModels method;
    /**
     * The model to use to generate trace links.
     */
    ModelAppEntity model;
}
