package edu.nd.crc.safa.features.github.entities.api.graphql;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.NONE)
public final class GithubGraphQlQueries {
    public static final String GET_REPOSITORIES = "github/GetRepositories";
    public static final String GET_REPOSITORY_BY_NAME = "github/GetRepositoryByName";
    public static final String GET_TREE_OBJECTS = "github/GetTreeObjects";
    public static final String PAGINATE_REPOSITORIES = "github/PaginateRepositories";
    public static final String PAGINATE_BRANCHES = "github/PaginateBranches";
}
