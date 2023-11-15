package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;

import lombok.Data;

public class GithubGraphQlFileContentsResponse extends GraphQlResponse<GithubGraphQlFileContentsResponse.Payload> {

    @Data
    public static class Payload {
        private TreeRepository repository;
    }

    @Data
    public static class TreeRepository {
        private FileObject object;
    }

    @Data
    public static class FileObject {
        private String text;
    }
}
