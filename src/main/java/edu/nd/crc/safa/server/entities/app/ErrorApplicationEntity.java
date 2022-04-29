package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * The Front-end version of an error.
 */
public class ErrorApplicationEntity {
    String errorId;
    String message;
    ProjectEntity activity;

    public ErrorApplicationEntity(CommitError error) {
        this.message = error.getDescription();
        this.errorId = error.getErrorId();
        this.activity = error.getApplicationActivity();
    }

    public String getErrorId() {
        return this.errorId;
    }

    public void setErrorId(String errorId) {
        this.errorId = errorId;
    }

    public String getMessage() {
        return this.message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public ProjectEntity getActivity() {
        return this.activity;
    }

    public void setActivity(ProjectEntity activity) {
        this.activity = activity;
    }

    public CommitError toCommitError(ProjectVersion projectVersion) {
        return new CommitError(projectVersion, this.message, this.activity);
    }

    public String toString() {
        return String.format("%s %s %s", this.errorId, this.message, this.activity);
    }
}
