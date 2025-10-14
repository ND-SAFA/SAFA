package edu.nd.crc.safa.features.errors.entities.app;

import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;

import lombok.Data;

/**
 * The Front-end version of an error.
 */
@Data
public class ErrorApplicationEntity {
    private String errorId;
    private String message;
    private ProjectEntityType activity;

    public ErrorApplicationEntity(CommitError error) {
        this.message = error.getDescription();
        this.errorId = error.getErrorId();
        this.activity = error.getApplicationActivity();
    }
}
