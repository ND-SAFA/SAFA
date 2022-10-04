package edu.nd.crc.safa.common;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.Map;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@AllArgsConstructor
@Service
public class SafaRequestBuilder {
    private final WebClient webClient;
    private final int DEFAULT_TIMEOUT = 30;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public <T> T sendPost(String endpoint,
                          Object object,
                          Class<T> responseClass) {
        // Step - Send request
        return sendJsonRequest(endpoint, object, responseClass, HttpMethod.POST);
    }

    public <T> T sendJsonRequest(String endpoint,
                                 Object object,
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
            object,
            responseClass,
            Duration.of(DEFAULT_TIMEOUT, ChronoUnit.SECONDS));

        // Step - Send request
        return sendRequest(requestMeta);
    }

    public <T> T sendRequest(RequestMeta<T> requestMeta) {
        WebClient.RequestBodySpec requestHeadersSpec = webClient
            .method(requestMeta.httpMethod)
            .uri(requestMeta.endpoint);

        if (requestMeta.payload != null) {
            requestHeadersSpec.bodyValue(requestMeta.payload);
        }

        for (Map.Entry<String, Object> keyValue : requestMeta.getHeaders().entrySet()) {
            requestHeadersSpec.header(keyValue.getKey(), keyValue.getValue().toString());
        }

        Mono<String> responseStr = requestHeadersSpec
            .retrieve()
            .bodyToMono(String.class);

        try {
            return objectMapper.readValue(responseStr.block(), requestMeta.responseClass);
        } catch (JsonProcessingException e) {
            throw new SafaError("Unable to parse TGEN response.", e);
        }
    }

    @AllArgsConstructor
    @Data
    class RequestMeta<T> {
        String endpoint;
        HttpMethod httpMethod;
        Map<String, Object> headers;
        Object payload;
        Class<T> responseClass;
        Duration timeout = Duration.of(DEFAULT_TIMEOUT, ChronoUnit.SECONDS);
    }
}
