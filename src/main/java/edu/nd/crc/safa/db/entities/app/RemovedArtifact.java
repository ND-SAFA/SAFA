package edu.nd.crc.safa.db.entities.app;

public class RemovedArtifact extends DeltaArtifact {

    String previous;

    public RemovedArtifact() {
    }

    public RemovedArtifact(String artifactId, String previous) {
        super(artifactId);
        this.previous = previous;
    }

    public String getPrevious() {
        return this.previous;
    }

    public void setPrevious(String previous) {
        this.previous = previous;
    }
}
