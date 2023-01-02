package edu.nd.crc.safa.features.github.entities.app;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Simple DTO to wrap status messages for GitHub operations
 */
@AllArgsConstructor
@Getter
public class GithubResponseDTO<T> {

    T payload;

    GithubResponseMessage message;

    @AllArgsConstructor
    public enum GithubResponseMessage {
        TOKEN_REFRESH_REQUIRED("Authorization token has expired. Please refresh."),
        CREATED("Created"),
        UPDATED("Updated"),
        OK("Ok"),
        ERROR("Error"),
        IMPORTED("Imported"),
        EXPIRED("Expired credentials. Will delete them"),
        MISSING("No credentials found"),
        DELETED("Deleted existing GitHub credentials");

        private final String value;
    }
}
