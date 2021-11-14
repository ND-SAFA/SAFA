package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/* Responsible for identifying error that were accounted
 * for in the execution of our application. Other error are
 * regarded as unaccounted for.
 */
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ServerError extends Exception {
    Exception exception;
    List<String> errors;
    String details;
    String message;

    public ServerError(String message) {
        this.message = message;
        this.errors = new ArrayList<>();
    }

    public ServerError(Exception e) {
        this.exception = e;
        this.errors =
            Arrays
                .stream(e.getStackTrace())
                .map(StackTraceElement::toString)
                .collect(Collectors.toList());
    }

    public ServerError(String message, Exception e) {
        this(e);
        this.message = message;
        this.errors.add(0, e.getLocalizedMessage());
        this.details = e.getMessage();
    }

    public void printError() {
        if (this.exception != null) {
            this.exception.printStackTrace();
        } else {
            this.printStackTrace();
        }
    }

    public String getMessage() {
        return this.message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getDetails() {
        return this.details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public List<String> getErrors() {
        return this.errors;
    }

    public void setErrors(List<String> newStackTrace) {
        this.errors = newStackTrace;
    }
}
