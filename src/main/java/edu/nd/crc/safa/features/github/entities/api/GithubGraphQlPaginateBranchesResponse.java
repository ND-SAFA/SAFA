package edu.nd.crc.safa.features.github.entities.api;

import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.utilities.graphql.entities.DefaultPaginatable;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;

import lombok.Data;

public class GithubGraphQlPaginateBranchesResponse
    extends GraphQlResponse<GithubGraphQlPaginateBranchesResponse.Payload> {

    @Data
    public static class Payload implements DefaultPaginatable {
        private Repository repository;
    }
}
