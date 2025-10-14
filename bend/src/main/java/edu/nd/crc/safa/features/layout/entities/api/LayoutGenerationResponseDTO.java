package edu.nd.crc.safa.features.layout.entities.api;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;

import lombok.Data;

/**
 * Response to regenerating the layout.
 */
@Data
public class LayoutGenerationResponseDTO {

    /**
     * Layout of default document if asked to be regenerated.
     */
    private Map<UUID, LayoutPosition> defaultDocumentLayout;
    /**
     * Map of document to its layout (map of artifact id to position).
     */
    private Map<UUID, Map<UUID, LayoutPosition>> documentLayoutMap;

    public void addDocumentLayout(UUID documentId, Map<UUID, LayoutPosition> layout) {
        if (this.documentLayoutMap == null) {
            this.documentLayoutMap = new HashMap<>();
        }
        this.documentLayoutMap.put(documentId, layout);
    }
}
