package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.ParserError;

public class ErrorApplicationEntity {
    String errorId;
    String message;
    String location;
    String activity;

    public ErrorApplicationEntity(ParserError error) {
        this.message = error.getDescription();
        this.location = error.getFileName();
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

    public String getLocation() {
        return this.location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getActivity() {
        return this.activity;
    }

    public void setActivity(String activity) {
        this.activity = activity;
    }
}
