package edu.nd.crc.safa.features.layout.entities.api;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import lombok.Data;

/**
 * Request to regenerate layout of entities defined.
 */
@Data
public class LayoutGenerationRequestDTO {
    /**
     * The id of the document to create.
     */
    private boolean defaultDocument = true;
    /**
     * Ids of document whose layouts are regenerated.
     */
    private List<UUID> documentIds = new ArrayList<>();
}
