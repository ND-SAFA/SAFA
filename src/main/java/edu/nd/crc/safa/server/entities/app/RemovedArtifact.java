package edu.nd.crc.safa.server.entities.app;

/**
 * Represents an artifact that was removed between two versions.
 */
public class RemovedArtifact extends DeltaArtifact {

    String before;
    String beforeSummary;

    public RemovedArtifact() {
    }

    public RemovedArtifact(String artifactId, String before, String beforeSummary) {
        super(artifactId);
        this.before = before;
        this.beforeSummary = beforeSummary;
    }

    public String getBefore() {
        return this.before;
    }

    public void setBefore(String before) {
        this.before = before;
    }

    public String getBeforeSummary() {
        return this.beforeSummary;
    }

    public void setBeforeSummary(String beforeSummary) {
        this.beforeSummary = beforeSummary;
    }
}
