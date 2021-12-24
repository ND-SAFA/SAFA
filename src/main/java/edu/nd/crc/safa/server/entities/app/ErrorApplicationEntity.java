package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.CommitError;

public class ErrorApplicationEntity {
    String errorId;
    String message;
    String activity;

    public ErrorApplicationEntity(CommitError error) {
        this.message = error.getDescription();
        this.errorId = error.getErrorId();
        this.activity = error.getApplicationActivity().toString();
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

    public String getActivity() {
        return this.activity;
    }

    public void setActivity(String activity) {
        this.activity = activity;
    }
}
