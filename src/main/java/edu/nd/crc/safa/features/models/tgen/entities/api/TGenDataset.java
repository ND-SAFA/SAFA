package edu.nd.crc.safa.features.models.tgen.entities.api;

import java.util.List;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TGenDataset {
    /**
     * Map of source artifact ids to content body.
     */
    List<Map<String, String>> sourceLayers;
    /**
     * Map of target artifact ids to content body.
     */
    List<Map<String, String>> targetLayers;
}
