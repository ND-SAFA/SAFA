package edu.nd.crc.safa.features.common;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

/**
 * Builds and performs HTTP/HTTPS requests.
 */
@AllArgsConstructor
@Service
public class RequestService {
    private final ObjectMapper objectMapper = ObjectMapperConfig.create();
    private final WebClient webClient;
    private final int DEFAULT_TIMEOUT = 60 * 60; // 1 Hour

    /**
     * Performs a POST request.
     *
     * @param endpoint      Where to send request to.
     * @param payload       The payload to send in body of request.
     * @param responseClass The expected class response should be in.
     * @param <T>           The type associated with response to parse.
     * @return The parsed of generic type.
     */
    public <T> T sendPost(String endpoint,
                          Object payload,
                          Class<T> responseClass) {
        // Step - Send request
        return sendJsonRequest(endpoint, payload, responseClass, HttpMethod.POST);
    }

    /**
     * Performs request with JSON headers.
     *
     * @param endpoint      The endpoint to send request to.
     * @param payload       The payload to send in request.
     * @param responseClass The expected class to parse response to.
     * @param method        The type of HTTP method to make request with.
     * @param <T>           The generic type to parse response to.
     * @return The parsed response.
     */
    public <T> T sendJsonRequest(String endpoint,
                                 Object payload,
                                 Class<T> responseClass,
                                 HttpMethod method) {
        // Step - Create headers
        Map<String, Object> headerMap = new HashMap<>();
        headerMap.put("Content-Type", MediaType.APPLICATION_JSON);
        headerMap.put("Accept", MediaType.APPLICATION_JSON);

        // Step - Build request

        RequestMeta<T> requestMeta = new RequestMeta<>(
            endpoint,
            method,
            headerMap,
            payload,
            responseClass,
            Duration.of(DEFAULT_TIMEOUT, ChronoUnit.SECONDS));

        // Step - Send request
        return sendRequest(requestMeta);
    }

    /**
     * Performs generic request.
     *
     * @param requestMeta Request meta details including endpoint, method, payload, and more.
     * @param <T>         The expected response type.
     * @return The parsed response.
     */
    public <T> T sendRequest(RequestMeta<T> requestMeta) {
        WebClient.RequestBodySpec request = webClient
            .method(requestMeta.httpMethod)
            .uri(requestMeta.endpoint);

        if (requestMeta.payload != null) {
            request.bodyValue(requestMeta.payload);
        }

        for (Map.Entry<String, Object> keyValue : requestMeta.getHeaders().entrySet()) {
            request.header(keyValue.getKey(), keyValue.getValue().toString());
        }

        Mono<String> responseMono = request.exchangeToMono(response -> {
            if (response.statusCode().is2xxSuccessful()) {
                return response.bodyToMono(String.class);
            } else if (response.statusCode().isError()) {
                return response.bodyToMono(String.class).flatMap(body -> {
                    String error = parseResponse(body, String.class);
                    return Mono.error(new RuntimeException(error));
                });
            } else {
                return Mono.error(new RuntimeException("HTTP Error " + response.statusCode().value()));
            }
        });

        String responseStr = responseMono.block();
        return parseResponse(responseStr, requestMeta.responseClass);
    }

    /**
     * Parses JSON string into target type.
     *
     * @param jsonString The JSON string.
     * @param targetType The target type being one of JavaType, TypeReference, or Class
     * @param <T>        The generic type to parse into
     * @return The target class referenced by type or class.
     */
    public <T> T parseResponse(String jsonString, Object targetType) {
        try {
            if (targetType instanceof JavaType) {
                return objectMapper.readValue(jsonString, (JavaType) targetType);
            } else if (targetType instanceof Class) {
                return objectMapper.readValue(jsonString, (Class<T>) targetType);
            } else if (targetType instanceof TypeReference) {
                return objectMapper.readValue(jsonString, (TypeReference<T>) targetType);
            } else {
                throw new IllegalArgumentException("Unsupported target type: " + targetType.getClass());
            }
        } catch (JsonProcessingException e) {
            throw new SafaError("Response not recognized.", e);
        }
    }

    @AllArgsConstructor
    @Data
    protected class RequestMeta<T> {
        private String endpoint;
        private HttpMethod httpMethod;
        private Map<String, Object> headers;
        private Object payload; // can be JavaType, TypeReference, or Class<T>
        private Object responseClass;
        private Duration timeout = Duration.of(DEFAULT_TIMEOUT, ChronoUnit.SECONDS);
    }
}
