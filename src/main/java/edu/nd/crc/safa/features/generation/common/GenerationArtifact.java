package edu.nd.crc.safa.features.generation.common;

import jakarta.annotation.Nullable;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The artifact representation for summarization.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@AllArgsConstructor
@NoArgsConstructor
public class GenerationArtifact {
    /**
     * The identifier of the artifact.
     */
    @Nullable
    private String id;
    /**
     * The content to summarize.
     */
    private String content;
    /**
     * The artifact summary.
     */
    private String summary;
    /**
     * The layer this artifact belongs to
     */
    @JsonProperty("layer_id")
    private String layerId;

    public GenerationArtifact(ArtifactAppEntity artifact) {
        this.id = artifact.getName();
        this.content = artifact.getBody();
        this.summary = artifact.getSummary();
        this.layerId = artifact.getType();
    }
}
