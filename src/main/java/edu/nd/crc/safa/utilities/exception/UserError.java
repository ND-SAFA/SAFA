package edu.nd.crc.safa.utilities.exception;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@Getter
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class UserError extends Exception {

    public UserError(String message) {
        super(message);
    }
}
