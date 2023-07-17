package edu.nd.crc.safa.features.generation.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Nullable;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The dataset used for the generation api.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class GenerationDataset {
    /**
     * Map of artifact type to artifact maps.
     */
    @JsonProperty("artifact_layers")
    Map<String, Map<String, String>> artifactLayers; // snake_case to match TGEN
    /**
     * List of layers being traced (child -> parent).
     */
    @JsonProperty()
    List<TraceLayer> layers;
    /**
     * The trace links between artifacts in all artifact layers.
     */
    @Nullable
    @JsonProperty("true_links")
    List<GenerationLink> trueLinks;
    /**
     * Optional. Project summary.
     */
    @Nullable
    String summary;

    @JsonIgnore
    Map<String, List<String>> layerIds = new HashMap<>();

    public GenerationDataset(Map<String, Map<String, String>> artifactLayers, List<TraceLayer> layers) {
        this.artifactLayers = artifactLayers;
        this.layers = layers;
    }

    public List<String> getArtifacts(String artifactType) {
        if (!this.layerIds.containsKey(artifactType)) {
            Map<String, String> artifactMap = this.artifactLayers.get(artifactType);
            List<String> artifacts = new ArrayList<>(artifactMap.values());
            this.layerIds.put(artifactType, artifacts);
        }
        return this.layerIds.get(artifactType);
    }

    /**
     * @return Returns the number of comparisons that are made for search or prediction.
     */
    @JsonIgnore
    public int getNumOfCandidates() {
        int nCandidates = 0;
        for (TraceLayer layer : this.layers) {
            Map<String, String> childArtifactMap = this.artifactLayers.get(layer.getChild());
            Map<String, String> parentArtifactMap = this.artifactLayers.get(layer.getParent());
            nCandidates += childArtifactMap.size() * parentArtifactMap.size();
        }
        return nCandidates;
    }
}
