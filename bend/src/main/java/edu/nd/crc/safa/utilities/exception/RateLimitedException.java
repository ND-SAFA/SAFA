package edu.nd.crc.safa.utilities.exception;

import java.time.Instant;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

public class RateLimitedException extends SafaError {
    public RateLimitedException() {
        super("External service is rate limiting us. Please try again later.");
    }

    public RateLimitedException(Instant retryInstant) {
        super("External service is rate limiting us. Please try again after " + retryInstant.toString());
    }
}
