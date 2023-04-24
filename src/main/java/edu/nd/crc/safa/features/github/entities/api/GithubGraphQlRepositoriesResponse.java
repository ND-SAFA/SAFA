package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.graphql.entities.Edges;
import edu.nd.crc.safa.features.graphql.entities.GraphQlResponse;

import lombok.Data;
import lombok.Getter;
import lombok.ToString;

/**
 * Response for {@code github/GetRepositories.graphql}.
 */
@Getter
@ToString
public class GithubGraphQlRepositoriesResponse extends GraphQlResponse<GithubGraphQlRepositoriesResponse.Payload> {

    @Data
    public static class Payload {

        private Viewer viewer;

        @Data
        public static class Viewer {
            private Edges<Repository> repositories;
        }
    }
}
