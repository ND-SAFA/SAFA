package edu.nd.crc.safa.features.github.services;

import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
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
        return makeGraphQlRequest(user,
            "github/GetRepositories",
            GithubGraphQlRepositoriesResponse.class);
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
        return makeGraphQlRequest(user,
            "github/GetRepositoryByName",
            GithubGraphQlRepositoryResponse.class,
            "repoOwner", owner,
            "repoName", name);
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
