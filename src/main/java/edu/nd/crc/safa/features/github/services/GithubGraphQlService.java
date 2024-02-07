package edu.nd.crc.safa.features.github.services;

import java.util.function.Function;
import java.util.logging.Logger;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlPaginateBranchesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlTreeObjectsResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.Branch;
import edu.nd.crc.safa.features.github.entities.api.graphql.GithubGraphQlQueries;
import edu.nd.crc.safa.features.github.entities.api.graphql.Repository;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.exception.ExternalAPIException;
import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
import edu.nd.crc.safa.utilities.graphql.services.GraphQlService;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;

@Service
public class GithubGraphQlService {

    private static final Logger logger = Logger.getLogger(GithubGraphQlService.class.getName());

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
     * <p>Get all objects within a tree under a specified path.</p>
     *
     * <p>The format for the path is {@code "branch:path"} where {@code path} is
     * the path within the repo. To get items at the top level, use {@code "branch:"}
     * (with no path)</p>
     *
     * <p>In order to get all files in a repository, this function must be called
     * repeatedly, once for the top level and again for every item with type "tree".</p>
     *
     * @param user The user making the request.
     * @param owner The owner of the repository.
     * @param name The name of the repository.
     * @param location The location of the files to get.
     * @return The tree objects.
     */
    public GithubGraphQlTreeObjectsResponse getGithubTreeObjects(SafaUser user, String owner,
                                                                 String name, String location) {
        return makeGraphQlRequest(user,
            GithubGraphQlQueries.GET_TREE_OBJECTS,
            GithubGraphQlTreeObjectsResponse.class,
            "repoOwner", owner,
            "repoName", name,
            "location", location);
    }

    /**
     * Paginate through all repositories the user has access to.
     *
     * @param user The user making the request.
     * @param edges The edges object we are expanding in this pagination.
     */
    public void paginateRepositories(SafaUser user, Edges<Repository> edges) {
        paginate(
            user,
            edges,
            GithubGraphQlRepositoriesResponse.class,
            GithubGraphQlQueries.PAGINATE_REPOSITORIES,
            response -> response.getData().getViewer().getRepositories());
    }

    /**
     * Paginate through all branches in a repository.
     *
     * @param user The user making the request.
     * @param repoName The name of the repository.
     * @param repoOwner The owner of the repository.
     * @param edges The edges object we are expanding in this pagination.
     */
    public void paginateBranches(SafaUser user, Edges<Branch> edges, String repoName, String repoOwner) {
        paginate(
            user,
            edges,
            GithubGraphQlPaginateBranchesResponse.class,
            GithubGraphQlQueries.PAGINATE_BRANCHES,
            response -> response.getData().getRepository().getRefs(),
            "repoName", repoName,
            "repoOwner", repoOwner);
    }

    /**
     * Performs pagination on the given edges variable with github authorization.
     *
     * @param user The user making the request.
     * @param edges The edges object we are expanding in this pagination.
     * @param responseClass The class that represents the schema that will be returned by the pagination query.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param edgesRetriever A function that retrieves the edges from the response.
     * @param variables Variables to be passed to the query.
     * @param <T> The type contained by edges.
     * @param <U> The type of the response.
     */
    private <T, U extends GraphQlResponse<?>> void paginate(SafaUser user, Edges<T> edges, Class<U> responseClass,
                                                            String queryLocation, Function<U, Edges<T>> edgesRetriever,
                                                            String... variables) {

        String authorization = getAuthorization(user);
        graphQlService.paginate(githubGraphqlUrl, queryLocation, authorization, responseClass,
            edges, edgesRetriever, variables);
    }

    /**
     * Makes a github graphql request.
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

        String authorization = getAuthorization(user);

        try {
            return graphQlService.makeGraphQlRequest(githubGraphqlUrl, queryLocation,
                authorization, responseClass, variables);
        } catch (ExternalAPIException ex) {
            if (ex.getResponseCode() == HttpStatusCode.valueOf(401)) {
                githubConnectionService.deleteGithubCredentials(user);
                throw new SafaError("GitHub credentials expired. Please re-authorize.");
            }
            throw ex;
        }
    }

    /**
     * Gets the authorization header for the user.
     *
     * @param user The user making the request.
     * @return The authorization header.
     */
    private String getAuthorization(SafaUser user) {
        GithubAccessCredentials githubAccessCredentials =
            githubConnectionService.getGithubCredentials(user)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));

        return String.format("token %s", githubAccessCredentials.getAccessToken());
    }
}
