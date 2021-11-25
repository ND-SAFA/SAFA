package edu.nd.crc.safa.server.entities.app;

/**
 * Represents the addition of an artifact between two project versions.
 * Namely, `after` is used to mean the target version in a delta comparison
 * although not necessarily having to occur later in time.
 */
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
