package edu.nd.crc.safa.db.entities.app;

public class ModifiedArtifact extends DeltaArtifact {

    String before;
    String after;

    public ModifiedArtifact() {
    }

    public ModifiedArtifact(String artifactId, String before, String after) {
        super(artifactId);
        this.before = before;
        this.after = after;
    }

    public String getBefore() {
        return this.before;
    }

    public void setBefore(String before) {
        this.before = before;
    }

    public String getAfter() {
        return this.after;
    }

    public void setAfter(String after) {
        this.after = after;
    }
}
