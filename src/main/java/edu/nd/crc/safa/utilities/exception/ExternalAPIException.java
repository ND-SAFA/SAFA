package edu.nd.crc.safa.utilities.exception;

import lombok.Getter;
import org.springframework.http.HttpStatusCode;

public class ExternalAPIException extends RuntimeException {

    @Getter
    private HttpStatusCode status;

    private String message;

    public ExternalAPIException(HttpStatusCode status, String message) {
        super(message);
        this.status = status;
        this.message = message;
    }

    public ExternalAPIException(String message, HttpStatusCode status, String message1) {
        super(message);
        this.status = status;
        this.message = message1;
    }
}
