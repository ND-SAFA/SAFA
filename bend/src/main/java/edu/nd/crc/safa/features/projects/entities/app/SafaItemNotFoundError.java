package edu.nd.crc.safa.features.projects.entities.app;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage", "exception", "errors"})
public class SafaItemNotFoundError extends SafaError {

    public SafaItemNotFoundError(String message) {
        super(message);
    }

    public SafaItemNotFoundError(String format, Object... args) {
        this(String.format(format.replace("%s", "[%s]"), args));
    }
}
