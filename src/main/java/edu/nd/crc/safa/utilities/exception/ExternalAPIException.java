package edu.nd.crc.safa.utilities.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

public class ExternalAPIException extends RuntimeException {

    @Getter
    HttpStatus status;

    String message;

    public ExternalAPIException(HttpStatus status, String message) {
        super(message);
        this.status = status;
        this.message = message;
    }

    public ExternalAPIException(String message, HttpStatus status, String message1) {
        super(message);
        this.status = status;
        this.message = message1;
    }
}
