package edu.nd.crc.safa.features.tgen.api;

import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;

import com.fasterxml.jackson.annotation.JsonProperty;
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
    @JsonProperty("source_layers")
    List<Map<String, String>> sourceLayers; // snake_case to match TGEN
    /**
     * Map of target artifact ids to content body.
     */
    @JsonProperty("target_layers")
    List<Map<String, String>> targetLayers; // snake_case to match TGEN
    /**
     * The trace links between artifacts in all artifact layers.
     */
    @Nullable
    @JsonProperty("true_links")
    List<List<String>> trueLinks;

    public TGenDataset(List<Map<String, String>> sourceLayers, List<Map<String, String>> targetLayers) {
        this.sourceLayers = sourceLayers;
        this.targetLayers = targetLayers;
    }
}
