package edu.nd.crc.safa.features.github.entities.api;

import java.util.List;

import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFileType;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

public class GithubGraphQlTreeObjectsResponse extends GraphQlResponse<GithubGraphQlTreeObjectsResponse.Payload> {

    @Data
    public static class Payload {
        private TreeRepository repository;
    }

    @Data
    public static class TreeRepository {
        private TreeObjects object;
    }

    @Data
    public static class TreeObjects {
        private List<Entry> entries;
    }

    @Data
    public static class Entry {
        private String name;
        private GithubRepositoryFileType type;
        private TreeObject object;
        private String path;
    }

    @Data
    public static class TreeObject {
        private String text;

        @JsonProperty("isBinary")  // Come on jackson why do I have to do this
        private boolean isBinary;
    }
}
