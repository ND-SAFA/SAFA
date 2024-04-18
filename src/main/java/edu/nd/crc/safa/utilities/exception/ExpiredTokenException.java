package edu.nd.crc.safa.utilities.exception;

import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@Getter
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ExpiredTokenException extends RuntimeException {
    private final LocalDateTime expiration;

    public ExpiredTokenException(LocalDateTime expiration) {
        super("Token expired");
        this.expiration = expiration;
    }
}
