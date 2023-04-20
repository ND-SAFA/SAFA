package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.List;

import lombok.Data;

@Data
public class GithubResponse<T> {
    private T data;
    private List<ResponseError> errors;

    @Data
    public static class ResponseError {
        private String type; // TODO enum
        private List<String> path;
        private List<ErrorLocation> locations;
        private String message;
    }

    @Data
    public static class ErrorLocation {
        private int line;
        private int column;
    }
}
