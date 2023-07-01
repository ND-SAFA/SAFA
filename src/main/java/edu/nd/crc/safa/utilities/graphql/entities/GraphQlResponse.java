package edu.nd.crc.safa.utilities.graphql.entities;

import java.util.List;

import lombok.Data;

@Data
public class GraphQlResponse<T> implements DefaultPaginatable {
    private T data;
    private List<ResponseError> errors;

    @Data
    public static class ResponseError {
        private String type;
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
