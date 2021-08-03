package edu.nd.crc.safa.server.error;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/* Responsible for identifying error that were accounted
 * for in the execution of our application. Other error are
 * regarded as unaccounted for.
 */
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ServerError extends Exception {
    String error;
    String message;

    public ServerError(String message) {
        this.message = message;
    }

    public ServerError(String activityName, Exception e) {
        this.message = String.format("An error occurred while %s.", activityName);
        this.error = e.getMessage();
    }

    public String getError() {
        return this.error = error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getMessage() {
        return this.message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
