package edu.nd.crc.safa.server.entities.api;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;

/**
 * Container for a request to generate trace links between artifacts.
 */
public class TraceLinkGenerationRequest {

    List<ArtifactAppEntity> sourceArtifacts;
    List<ArtifactAppEntity> targetArtifacts;

    public TraceLinkGenerationRequest() {
    }

    public List<ArtifactAppEntity> getSourceArtifacts() {
        return sourceArtifacts;
    }

    public void setSourceArtifacts(List<ArtifactAppEntity> sourceArtifacts) {
        this.sourceArtifacts = sourceArtifacts;
    }

    public List<ArtifactAppEntity> getTargetArtifacts() {
        return targetArtifacts;
    }

    public void setTargetArtifacts(List<ArtifactAppEntity> targetArtifacts) {
        this.targetArtifacts = targetArtifacts;
    }
}
