package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.graphql.entities.GraphQlResponse;

import lombok.Data;

/**
 * Response for {@code github/GetRepositoryByName.graphql}.
 */
public class GithubGraphQlRepositoryResponse extends GraphQlResponse<GithubGraphQlRepositoryResponse.Payload> {

    @Data
    public static class Payload {
        private Repository repository;
    }
}
