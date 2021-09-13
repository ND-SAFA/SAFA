package edu.nd.crc.safa.server.db.entities.app;

public class AddedArtifact extends DeltaArtifact {

    String after;
    String afterSummary;

    public AddedArtifact() {
    }

    public AddedArtifact(String artifactId, String after, String afterSummary) {
        super(artifactId);
        this.after = after;
        this.afterSummary = afterSummary;
    }

    public String getAfter() {
        return this.after;
    }

    public void setAfter(String after) {
        this.after = after;
    }

    public String getAfterSummary() {
        return this.afterSummary;
    }

    public void setAfterSummary(String afterSummary) {
        this.afterSummary = afterSummary;
    }
}
