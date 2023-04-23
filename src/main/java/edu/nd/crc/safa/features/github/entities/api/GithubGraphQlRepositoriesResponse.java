package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.github.entities.api.graphql.Edges;
import edu.nd.crc.safa.features.github.entities.api.graphql.GithubResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;

import lombok.Data;
import lombok.Getter;
import lombok.ToString;

/**
 * Response for {@code github/GetRepositories.graphql}.
 */
@Getter
@ToString
public class GithubGraphQlRepositoriesResponse extends GithubResponse<GithubGraphQlRepositoriesResponse.Payload> {

    @Data
    public static class Payload {

        private Viewer viewer;

        @Data
        public static class Viewer {
            private Edges<Repository> repositories;
        }
    }
}
