package edu.nd.crc.safa.utilities.graphql.services;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.logging.Logger;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.exception.ExternalAPIException;
import edu.nd.crc.safa.utilities.exception.RateLimitedException;
import edu.nd.crc.safa.utilities.graphql.entities.EdgeNode;
import edu.nd.crc.safa.utilities.graphql.entities.Edges;
import edu.nd.crc.safa.utilities.graphql.entities.GraphQlResponse;
import edu.nd.crc.safa.utilities.graphql.entities.PageInfo;
import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Mono;

@Service
@AllArgsConstructor
public class GraphQlService {

    private static final Logger logger = Logger.getLogger(GraphQlService.class.getName());

    private static final int NUM_RETRIES = 3;

    private final WebClient webClient;

    /**
     * Perform pagination on a list of edges from a previous request. This method is provided to cut down
     * on repeated code, but it requires many parameters to make it work. Many of the items are the same or
     * similar to {@link #makeGraphQlRequest(String, String, String, Class, String...)}.
     *
     * @param url The url for the GraphQL request that will get more items.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the pagination query definition.
     *                      The pagination query must have a variable named {@code "after"} which specifies where
     *                      the end cursor from the previous request goes.
     * @param authorization The authorization header to send with the request.
     *                      Can be null if no authorization is needed.
     * @param responseClass The class that represents the schema that will be returned by the pagination query.
     * @param edges The {@link Edges} object that we are performing pagination on.
     * @param edgesRetriever Given the response from a pagination query, this function retrieves the {@link Edges}
     *                       object which represents the new edges we have just retrieved.
     * @param variables Addition variables that will be passed to the query.
     * @param <T> The type the {@link Edges} object contains.
     * @param <U> The type of the response of the pagination query.
     */
    public <T, U extends GraphQlResponse<?>> void paginate(String url, String queryLocation, String authorization,
                                                           Class<U> responseClass, Edges<T> edges,
                                                           Function<U, Edges<T>> edgesRetriever,
                                                           String... variables) {

        // It would almost be possible to put this code in Edges
        // as it provides most of the information we need, but some queries
        // need extra parameters, so we need to have different instantiations
        // for everything we want to paginate. This function pulls together all
        // the common parts.

        PageInfo pageInfo = edges.getPageInfo();
        List<EdgeNode<T>> currentList = edges.getEdges();

        while (pageInfo.hasNextPage()) {
            List<String> variablesList = new ArrayList<>(List.of(variables));
            variablesList.add("after");
            variablesList.add(pageInfo.getEndCursor());

            U response = makeGraphQlRequest(url,
                queryLocation,
                authorization,
                responseClass,
                variablesList.toArray(new String[0]));

            Edges<T> newEdges = edgesRetriever.apply(response);
            currentList.addAll(newEdges.getEdges());
            pageInfo = newEdges.getPageInfo();
        }
    }

    /**
     * Performs a request against a GraphQL endpoint. Users should be aware of if their query
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
        return makeGraphQlRequest(url, queryLocation, authorization, responseClass, NUM_RETRIES, variables);
    }

    /**
     * Performs a request against a GraphQL endpoint. Users should be aware of if their query
     * will require pagination or not, and if so, they should call {@link Paginatable#paginate(SafaUser)}
     * to make sure pagination is handled. When in doubt, perform the pagination, unless you are already
     * within a pagination loop.
     *
     * @param url The url to send the request to.
     * @param queryLocation Location relative to {@code src/main/resources/graphql} of the query definition.
     * @param authorization The authorization header to send with the request.
     *                      Can be null if no authorization is needed.
     * @param responseClass The class that represents the schema that will be returned by the query.
     * @param retries The number of times to retry the query before giving up
     * @param variables Variables to be passed to the query.
     * @param <T> The query return type.
     * @return The result of the query.
     */
    public <T extends GraphQlResponse<?>> T makeGraphQlRequest(String url, String queryLocation,
                                                               String authorization, Class<T> responseClass,
                                                               int retries, String... variables)  {

        GraphqlRequestBody graphQLRequestBody = new GraphqlRequestBody();
        graphQLRequestBody.setQuery(loadQueryFromFile(queryLocation));
        addVariables(graphQLRequestBody, variables);

        Mono<T> request = createRequest(url, authorization, graphQLRequestBody, responseClass)
            .retry(retries);
        T response = request.block();
        resolveErrors(response);
        return response;
    }

    private <T extends GraphQlResponse<?>> void resolveErrors(T response) {
        if (response != null && response.getData() == null
            && response.getErrors() != null && !response.getErrors().isEmpty()) {

            // TODO this could probably be more robust
            throw new SafaError("The following errors were returned when trying to make the request: "
                + response.getErrors());
        }
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
            .toEntity(responseClass)
            .doOnSuccess(response -> checkRateLimit(url, response.getHeaders()))
            .mapNotNull(HttpEntity::getBody)
            .onErrorMap(ex -> ex instanceof WebClientResponseException, ex -> {
                WebClientResponseException responseException = (WebClientResponseException) ex;
                return new ExternalAPIException(responseException.getMessage(), responseException.getStatusCode(),
                    responseException.getResponseBodyAsString());
            });
    }

    private void checkRateLimit(String url, HttpHeaders headers) {
        List<String> values = headers.get("X-RateLimit-Remaining");
        if (values != null && !values.isEmpty()) {
            int remaining = Integer.parseInt(values.get(0));

            if (remaining == 0) {
                List<String> resetValues = headers.get("X-RateLimit-Reset");
                if (resetValues != null && !resetValues.isEmpty()) {
                    long resetTimestamp = Long.parseLong(resetValues.get(0));
                    throw new RateLimitedException(Instant.ofEpochSecond(resetTimestamp));
                } else {
                    throw new RateLimitedException();
                }
            }
            if (remaining < 100) {
                logger.warning(String.format("Remaining calls to %s: %d", url, remaining));
            }
        }
    }

    @Data
    private static class GraphqlRequestBody {
        private String query;
        private Map<String, String> variables = new HashMap<>();
    }
}
