package edu.nd.crc.safa.features.generation.common;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.annotation.Nullable;
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
    private List<GenerationArtifact> artifacts = new ArrayList<>(); // snake_case to match TGEN
    /**
     * The trace links between artifacts in all artifact layers.
     */
    @Nullable
    private List<GenerationLink> links = new ArrayList<>();
    /**
     * Optional. Project summary.
     */
    @Nullable
    private String summary = null;
    /**
     * List of layers being traced (child -> parent).
     */
    @JsonProperty()
    private List<TraceLayer> layers = new ArrayList<>();

    @JsonIgnore
    private Map<String, List<String>> layerIds = new HashMap<>();

    public GenerationDataset(List<GenerationArtifact> artifacts) {
        this.links = new ArrayList<>();
        this.layers = new ArrayList<>();
        this.artifacts = artifacts;
    }

    public GenerationDataset(List<GenerationArtifact> artifacts, List<TraceLayer> layers) {
        this.artifacts = artifacts;
        this.layers = layers;
    }

    public List<GenerationArtifact> getArtifacts(String artifactType) {
        return this.artifacts
            .stream()
            .filter(a -> a.getLayerId().equals(artifactType))
            .collect(Collectors.toList());
    }

    /**
     * @return Returns the number of comparisons that are made for search or prediction.
     */
    @JsonIgnore
    public int getNumOfCandidates() {
        int nCandidates = 0;
        for (TraceLayer layer : this.layers) {
            List<GenerationArtifact> childArtifacts = this.getArtifacts(layer.getChild());
            List<GenerationArtifact> parentArtifacts = this.getArtifacts(layer.getParent());
            nCandidates += childArtifacts.size() * parentArtifacts.size();
        }
        return nCandidates;
    }
}
