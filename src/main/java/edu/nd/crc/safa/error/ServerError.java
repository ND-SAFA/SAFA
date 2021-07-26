package edu.nd.crc.safa.error;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/* Responsible for identifying error that were accounted
 * for in the execution of our application. Other error are
 * regarded as unaccounted for.
 */
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ServerError extends Exception {
    Exception error;
    String message;

    public ServerError(String message) {
        this.message = message;
    }

    public ServerError(String activityName, Exception e) {
        this.message = String.format("Could not perform %s due to an error", activityName);
        this.error = e;
    }

    public Exception getError() {
        return this.error = error;
    }

    public void setError(Exception error) {
        this.error = error;
    }

    public String getMessage() {
        return this.message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
