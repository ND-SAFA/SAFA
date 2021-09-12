package edu.nd.crc.safa.server.db.entities.app;

public class AddedArtifact extends DeltaArtifact {

    String after;

    public AddedArtifact() {
    }

    public AddedArtifact(String artifactId, String previous) {
        super(artifactId);
        this.after = previous;
    }

    public String getAfter() {
        return this.after;
    }

    public void setAfter(String after) {
        this.after = after;
    }
}
