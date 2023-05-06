package edu.nd.crc.safa.features.github.services;

import java.util.List;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlPaginateBranchesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.Branch;
import edu.nd.crc.safa.features.github.entities.api.graphql.GithubGraphQlQueries;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.graphql.entities.EdgeNode;
import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
import edu.nd.crc.safa.utilities.graphql.entities.PageInfo;
import edu.nd.crc.safa.utilities.graphql.services.GraphQlService;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class GithubGraphQlService {

    @Value("${integrations.github.graphql-url}")
    private String githubGraphqlUrl;

    private final GraphQlService graphQlService;
    private final GithubConnectionService githubConnectionService;

    public GithubGraphQlService(GraphQlService graphQlService, GithubConnectionService githubConnectionService) {
        this.graphQlService = graphQlService;
        this.githubConnectionService = githubConnectionService;
    }

    /**
     * Get all repositories the user has access to.
     *
     * @param user The user making the request.
     * @return The repositories the user has access to.
     */
    public GithubGraphQlRepositoriesResponse getGithubRepositories(SafaUser user) {
        GithubGraphQlRepositoriesResponse response = makeGraphQlRequest(user,
            GithubGraphQlQueries.GET_REPOSITORIES,
            GithubGraphQlRepositoriesResponse.class);

        response.paginate(user);
        return response;
    }

    /**
     * Get a specific repository by owner and name.
     *
     * @param user The user making the request.
     * @param owner The owner of the repository.
     * @param name The name of the repository.
     * @return The repository.
     */
    public GithubGraphQlRepositoryResponse getGithubRepository(SafaUser user, String owner, String name) {
        GithubGraphQlRepositoryResponse response = makeGraphQlRequest(user,
            GithubGraphQlQueries.GET_REPOSITORY_BY_NAME,
            GithubGraphQlRepositoryResponse.class,
            "repoOwner", owner,
            "repoName", name);

        response.paginate(user);
        return response;
    }

    /**
     * Paginate through all repositories the user has access to.
     *
     * @param user The user making the request.
     * @param currentRepositories The current list of repositories from the original request.
     * @param pageInfo The page info from the original request.
     */
    public void paginateRepositories(SafaUser user, List<EdgeNode<Repository>> currentRepositories, PageInfo pageInfo) {
        while (pageInfo.hasNextPage()) {
            GithubGraphQlRepositoriesResponse response = makeGraphQlRequest(user,
                GithubGraphQlQueries.PAGINATE_REPOSITORIES,
                GithubGraphQlRepositoriesResponse.class,
                "after", pageInfo.getEndCursor());

            Edges<Repository> repositoryEdges = response.getData().getViewer().getRepositories();
            currentRepositories.addAll(repositoryEdges.getEdges());
            pageInfo = repositoryEdges.getPageInfo();
        }
    }

    /**
     * Paginate through all branches in a repository.
     *
     * @param user The user making the request.
     * @param currentBranches The current list of branches from the original request.
     * @param repoName The name of the repository.
     * @param repoOwner The owner of the repository.
     * @param pageInfo The page info from the original request.
     */
    public void paginateBranches(SafaUser user, List<EdgeNode<Branch>> currentBranches, String repoName,
                                 String repoOwner, PageInfo pageInfo) {
        while (pageInfo.hasNextPage()) {
            GithubGraphQlPaginateBranchesResponse response = makeGraphQlRequest(user,
                GithubGraphQlQueries.PAGINATE_BRANCHES,
                GithubGraphQlPaginateBranchesResponse.class,
                "after", pageInfo.getEndCursor(),
                "repoName", repoName,
                "repoOwner", repoOwner);

            Edges<Branch> branches = response.getData().getRepository().getRefs();
            currentBranches.addAll(branches.getEdges());
            pageInfo = branches.getPageInfo();
        }
    }

    /**
     * Makes q github graphql request.
     *
     * @param user The user making the request.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param variables Variables to be passed to the query.
     * @param <T> The query return type.
     * @return The result of the query.
     */
    private <T extends GraphQlResponse<?>> T makeGraphQlRequest(SafaUser user, String queryLocation,
                                                                Class<T> responseClass, String... variables) {
        GithubAccessCredentials githubAccessCredentials =
            githubConnectionService.getGithubCredentials(user)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));

        String authorization = String.format("token %s", githubAccessCredentials.getAccessToken());

        return graphQlService.makeGraphQlRequest(githubGraphqlUrl, queryLocation,
            authorization, responseClass, variables);
    }
}
