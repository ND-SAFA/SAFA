package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.github.entities.api.graphql.GithubResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;

import lombok.Data;

public class GithubGraphQlRepositoryResponse extends GithubResponse<GithubGraphQlRepositoryResponse.Payload> {

    @Data
    public static class Payload {
        private Repository repository;
    }
}
