package edu.nd.crc.safa.features.projects.entities.app;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Responsible for identifying error that were accounted
 * for in the execution of our application. Other error are
 * regarded as unaccounted for.
 */
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
@Data
@EqualsAndHashCode(callSuper = false)
public class SafaError extends RuntimeException {
    private final Exception exception;
    private final List<String> errors;
    private final String message;

    public SafaError(String message) {
        this.message = message;
        this.exception = null;
        this.errors = new ArrayList<>();
    }

    public SafaError(String format, Object... args) {
        this(String.format(format.replace("%s", "[%s]"), args));
    }

    public SafaError(String message, Exception e) {
        this.exception = e;
        this.message = message;
        this.errors =
            Arrays
                .stream(e.getStackTrace())
                .map(StackTraceElement::toString)
                .collect(Collectors.toList());
        this.errors.add(0, e.getLocalizedMessage());
    }

    public void printError() {
        Objects.requireNonNullElse(this.exception, this).printStackTrace();
    }
}
