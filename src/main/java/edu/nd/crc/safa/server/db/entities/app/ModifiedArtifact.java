package edu.nd.crc.safa.server.db.entities.app;

public class ModifiedArtifact extends DeltaArtifact {

    String before;
    String beforeSummary;
    String after;
    String afterSummary;

    public ModifiedArtifact() {
    }

    public ModifiedArtifact(String artifactId,
                            String before,
                            String beforeSummary,
                            String after,
                            String afterSummary) {
        super(artifactId);
        this.before = before;
        this.beforeSummary = beforeSummary;
        this.after = after;
        this.afterSummary = afterSummary;
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
