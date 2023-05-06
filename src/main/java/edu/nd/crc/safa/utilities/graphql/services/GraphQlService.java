package edu.nd.crc.safa.utilities.graphql.services;

import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
@AllArgsConstructor
public class GraphQlService {

    private final WebClient webClient;

    /**
     * Performs a request against the GitHub GraphQL endpoint. Users should be aware of if their query
     * will require pagination or not, and if so, they should call {@link Paginatable#paginate(SafaUser)}
     * to make sure pagination is handled. When in doubt, perform the pagination, unless you are already
     * within a pagination loop.
     *
     * @param url The url to send the request to.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param authorization The authorization header to send with the request.
     *                      Can be null if no authorization is needed.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param variables Variables to be passed to the query.
     * @param <T> The query return type.
     * @return The result of the query.
     */
    public <T extends GraphQlResponse<?>> T makeGraphQlRequest(String url, String queryLocation,
                                                               String authorization, Class<T> responseClass,
                                                               String... variables)  {

        GraphqlRequestBody graphQLRequestBody = new GraphqlRequestBody();
        graphQLRequestBody.setQuery(loadQueryFromFile(queryLocation));
        addVariables(graphQLRequestBody, variables);

        return createRequest(url, authorization, graphQLRequestBody, responseClass).block();
    }

    /**
     * Loads a query schema from a file.
     *
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @return The query schema.
     */
    private String loadQueryFromFile(String queryLocation) {
        try {
            String resourcePath = "graphql/" + queryLocation + ".graphql";
            return FileUtilities.readClasspathFile(resourcePath);
        }  catch (Exception e) {
            throw new SafaError("Could not load query schema", e);
        }
    }

    /**
     * Adds variables to the GraphQL request body.
     *
     * @param graphQLRequestBody The GraphQL request body.
     * @param variables The variables to add.
     */
    private void addVariables(GraphqlRequestBody graphQLRequestBody, String... variables) {
        assert variables.length % 2 == 0;
        for (int i = 0; i < variables.length; i += 2) {
            String variableName = variables[i];
            String variableValue = variables[i + 1];
            graphQLRequestBody.getVariables().put(variableName, variableValue);
        }
    }

    /**
     * Creates a request to the GitHub GraphQL endpoint.
     *
     * @param url The url to send the request to.
     * @param authorization The authorization header to send with the request.
     * @param graphQLRequestBody The GraphQL request body.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param <T> The query return type.
     * @return The response from the request.
     */
    private <T extends GraphQlResponse<?>> Mono<T> createRequest(String url, String authorization,
                                                                 GraphqlRequestBody graphQLRequestBody,
                                                                 Class<T> responseClass) {

        WebClient.RequestBodySpec requestBodySpec = webClient.post().uri(url);

        if (authorization != null) {
            requestBodySpec = requestBodySpec.header(HttpHeaders.AUTHORIZATION, authorization);
        }

        return requestBodySpec
            .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .bodyValue(graphQLRequestBody)
            .retrieve()
            .bodyToMono(responseClass);
    }

    @Data
    private static class GraphqlRequestBody {
        private String query;
        private Map<String, String> variables = new HashMap<>();
    }
}
