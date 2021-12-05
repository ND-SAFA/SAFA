package edu.nd.crc.safa.server.entities.app;

/**
 * The base model for representing a way an artifact can change between versions.
 */
public class DeltaArtifact implements IDeltaEntity {

    String artifactId;

    public DeltaArtifact() {

    }

    public DeltaArtifact(String artifactId) {
        this.artifactId = artifactId;
    }

    public String getArtifactId() {
        return this.artifactId;
    }

    public void setArtifactId(String artifactId) {
        this.artifactId = artifactId;
    }
}
