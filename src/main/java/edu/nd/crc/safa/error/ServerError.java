package edu.nd.crc.safa.error;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/* Responsible for identifying error that were accounted
 * for in the execution of our application. Other error are
 * regarded as unaccounted for.
 */
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ServerError extends Exception {
    String error;
    String type;
    String message;

    public ServerError(String error) {
        this.error = error;
        this.type = "Internal";
    }

    public ServerError(String activityName, Exception e) {
        this.message = e.getMessage();
        this.type = e.getClass().toString();
        this.error = String.format("Could not perform %s due to a %s", activityName, this.message);
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

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
