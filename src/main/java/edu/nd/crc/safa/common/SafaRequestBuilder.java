package edu.nd.crc.safa.common;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@AllArgsConstructor
@Service
public class SafaRequestBuilder {
    private final WebClient webClient;
    private final int DEFAULT_TIMEOUT = 30;

    public <T> T sendPost(String endpoint,
                          Object object,
                          Class<T> responseClass) {
        // Step - Create headers
        Map<String, Object> headerMap = new HashMap<>();
        headerMap.put("Content-Type", MediaType.APPLICATION_JSON);
        headerMap.put("Accept", MediaType.APPLICATION_JSON);

        // Step - Build request

        RequestMeta<T> requestMeta = new RequestMeta<>(
            endpoint,
            HttpMethod.POST,
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

        ResponseEntity<T> response = requestHeadersSpec
            .retrieve()
            .toEntity(requestMeta.responseClass)
            .timeout(requestMeta.timeout)
            .block();

        // check response status code
        if (response != null
            && response.getStatusCode() != HttpStatus.BAD_REQUEST) {
            return response.getBody();
        } else {
            return null;
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
