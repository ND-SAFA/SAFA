package edu.nd.crc.safa.utilities.graphql.services;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
@AllArgsConstructor
public class GraphQlService {

    private final WebClient webClient;

    /**
     * Performs a request against the GitHub GraphQL endpoint.
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
    public <T> T makeGraphQlRequest(String url, String queryLocation, String authorization,
                                    Class<T> responseClass, String... variables)  {


        GraphqlRequestBody graphQLRequestBody = new GraphqlRequestBody();

        String query;
        try {
            query = GraphqlSchemaReaderUtil.getSchemaFromFileName(queryLocation);
        }  catch (Exception e) {
            throw new SafaError("Could not load query schema", e);
        }
        graphQLRequestBody.setQuery(query);

        assert variables.length % 2 == 0;
        for (int i = 0; i < variables.length; i += 2) {
            String variableName = variables[i];
            String variableValue = variables[i + 1];
            graphQLRequestBody.getVariables().put(variableName, variableValue);
        }

        WebClient.RequestBodySpec responseBodySpec = webClient.post().uri(url);

        if (authorization != null) {
            responseBodySpec = responseBodySpec.header(HttpHeaders.AUTHORIZATION, authorization);
        }

        return responseBodySpec
            .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .bodyValue(graphQLRequestBody)
            .retrieve()
            .bodyToMono(responseClass)
            .block();
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

    @Data
    private static class GraphqlRequestBody {
        private String query;
        private Map<String, String> variables = new HashMap<>();
    }
}
