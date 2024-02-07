package edu.nd.crc.safa.utilities.exception;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import org.springframework.http.HttpStatusCode;

@Getter
@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
public class ExternalAPIException extends RuntimeException {

    private final HttpStatusCode responseCode;

    private final String response;

    public ExternalAPIException(HttpStatusCode responseCode, String message) {
        super(message);
        this.responseCode = responseCode;
        this.response = "";
    }

    public ExternalAPIException(String message, HttpStatusCode responseCode, String response) {
        super(message);
        this.responseCode = responseCode;
        this.response = response;
    }
}
