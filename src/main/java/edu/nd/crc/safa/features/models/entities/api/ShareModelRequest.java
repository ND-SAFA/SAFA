package edu.nd.crc.safa.features.models.entities.api;

import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.ModelAppEntity;
import edu.nd.crc.safa.features.models.entities.ShareMethod;

import lombok.Data;

/**
 * Represents a request to share a model to a target project.
 */
@Data
public class ShareModelRequest {
    /**
     * The model to be shared.
     */
    ModelAppEntity model;
    /**
     * The project to share the model with.
     */
    UUID targetProject;
    /**
     * The method to share the model by.
     */
    ShareMethod shareMethod;
}
