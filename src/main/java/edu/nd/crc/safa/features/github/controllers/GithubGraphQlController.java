package edu.nd.crc.safa.features.github.controllers;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoriesResponse;
import edu.nd.crc.safa.features.github.entities.api.GithubGraphQlRepositoryResponse;
import edu.nd.crc.safa.features.github.entities.api.graphql.GithubResponse;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.context.request.async.DeferredResult;
import org.springframework.web.reactive.function.client.WebClient;

// TODO change endpoints to be the real ones

@Controller
public class GithubGraphQlController extends BaseController {
    private final ExecutorDelegate executorDelegate;
    private final SafaUserService safaUserService;
    private final GithubConnectionService githubConnectionService;
    private final WebClient webClient;

    @Value("${integrations.github.graphql-url}")
    private String githubGraphqlUrl;

    public GithubGraphQlController(ResourceBuilder resourceBuilder,
                                   ServiceProvider serviceProvider,
                                   ExecutorDelegate executorDelegate,
                                   WebClient webClient) {

        super(resourceBuilder, serviceProvider);
        this.executorDelegate = executorDelegate;
        this.webClient = webClient;

        this.safaUserService = serviceProvider.getSafaUserService();
        this.githubConnectionService = serviceProvider.getGithubConnectionService();
    }

    /**
     * Get all projects the user has access to.
     *
     * @return Accessible projects.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.ROOT)
    public DeferredResult<List<GithubRepositoryDTO>> retrieveGithubRepositories() {
        return makeDeferredRequest("github/GetRepositories",
            GithubGraphQlRepositoriesResponse.class,
            GithubRepositoryDTO::fromGraphQlResponse);
    }

    /**
     * Get a specific repo by owner and name.
     *
     * @param owner The owner of the project.
     * @param repo The name of the project.
     * @return The repo.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.BY_OWNER_AND_NAME)
    public DeferredResult<GithubRepositoryDTO> retrieveGithubRepository(@PathVariable("owner") String owner,
                                                                        @PathVariable("repo") String repo) {
        return makeDeferredRequest("github/GetRepositoryByName",
            GithubGraphQlRepositoryResponse.class,
            GithubRepositoryDTO::fromGraphQlResponse,
            "repoOwner", owner,
            "repoName", repo);
    }

    /**
     * Perform a deferred GraphQL request which will make the request with the given query schema,
     * transform it to the desired output type, and then return it.
     *
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param resultTransformer A function that will transform the returned data into the required data.
     * @param variables Variables to be passed to the query.
     * @param <T> The desired output type.
     * @param <R> The GraphQL return type.
     * @return A deferred result that will perform the above steps.
     */
    private <T, R extends GithubResponse<?>> DeferredResult<T> makeDeferredRequest(String queryLocation,
                                                                                   Class<R> responseClass,
                                                                                   Function<R, T> resultTransformer,
                                                                                   String... variables) {

        DeferredResult<T> output = executorDelegate.createOutput(5000L);

        SafaUser user = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {

            R response = makeGraphQlRequest(user, queryLocation, responseClass, variables);
            T result = resultTransformer.apply(response);

            output.setResult(result);
        });

        return output;
    }

    /**
     * Perform a deferred GraphQL request which will make the request with the given query schema
     * and return the result. This is the same as {@link #makeDeferredRequest(String, Class, Function, String...)}
     * except the transformer is just the identity function.
     *
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param variables Variables to be passed to the query.
     * @param <T> The query return type.
     * @return A deferred result that will perform the above steps.
     */
    private <T extends GithubResponse<?>> DeferredResult<T> makeDeferredRequest(String queryLocation,
                                                                                Class<T> responseClass,
                                                                                String... variables) {
        return makeDeferredRequest(queryLocation, responseClass, Function.identity(), variables);
    }

    /**
     * Performs a request against the GitHub GraphQL endpoint.
     *
     * @param user The safa user making the request.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param reponseClass The class that represents the schema that will be returned by the query.
     * @param variables Variables to be passed to the query.
     * @param <T> The query return type.
     * @return The result of the query.
     * @throws IOException In the case of failing to load the query.
     */
    private <T extends GithubResponse<?>> T makeGraphQlRequest(SafaUser user,
                                                               String queryLocation,
                                                               Class<T> reponseClass,
                                                               String... variables) throws IOException {
        GithubAccessCredentials githubAccessCredentials =
            githubConnectionService.getGithubCredentials(user)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));

        GraphqlRequestBody graphQLRequestBody = new GraphqlRequestBody();

        String query = GraphqlSchemaReaderUtil.getSchemaFromFileName(queryLocation);
        graphQLRequestBody.setQuery(query);
        
        assert variables.length % 2 == 0;
        for (int i = 0; i < variables.length; i += 2) {
            String variableName = variables[i];
            String variableValue = variables[i + 1];
            graphQLRequestBody.getVariables().put(variableName, variableValue);
        }

        return webClient.post()
            .uri(githubGraphqlUrl)
            .header(HttpHeaders.AUTHORIZATION, String.format("token %s", githubAccessCredentials.getAccessToken()))
            .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .bodyValue(graphQLRequestBody)
            .retrieve()
            .bodyToMono(reponseClass)
            .block();
    }

    @Data
    private static class GraphqlRequestBody {
        private String query;
        private Map<String, String> variables = new HashMap<>();
    }

    /**
     * Loads a graphql query definition from disk.
     */
    // TODO profile this to make sure we aren't taking the hit of going to disk on EVERY request
    private static final class GraphqlSchemaReaderUtil {

        public static String getSchemaFromFileName(String filename) throws IOException {
            ClassLoader classLoader = GraphqlSchemaReaderUtil.class.getClassLoader();
            String resourcePath = "graphql/" + filename + ".graphql";

            try (InputStream in = classLoader.getResourceAsStream(resourcePath)) {
                assert in != null;
                return new String(in.readAllBytes());
            }
        }
    }
}
