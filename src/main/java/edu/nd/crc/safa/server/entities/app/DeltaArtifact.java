package edu.nd.crc.safa.server.entities.app;

public class DeltaArtifact {

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
