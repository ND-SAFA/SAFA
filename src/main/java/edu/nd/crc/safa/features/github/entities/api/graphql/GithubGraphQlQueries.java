package edu.nd.crc.safa.features.github.entities.api.graphql;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public final class GithubGraphQlQueries {
    public static final String GET_REPOSITORIES = "github/GetRepositories";
    public static final String GET_REPOSITORY_BY_NAME = "github/GetRepositoryByName";
}
