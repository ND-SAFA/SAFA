package edu.nd.crc.safa.features.common;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

/**
 * The generic response from TGEN.
 */
@Data
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
class SafaResponse<T> {
    @JsonProperty("job_id")
    UUID jobId;
    int status;
    T body;
}

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
        WebClient.RequestBodySpec request = webClient
            .method(requestMeta.httpMethod)
            .uri(requestMeta.endpoint);

        if (requestMeta.payload != null) {
            ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();
            String json = null;
            try {
                json = ow.writeValueAsString(requestMeta.payload);
            } catch (JsonProcessingException e) {
                e.printStackTrace();
            }
            System.out.println("PAYLOAD:" + json);
            request.bodyValue(requestMeta.payload);
        }

        for (Map.Entry<String, Object> keyValue : requestMeta.getHeaders().entrySet()) {
            request.header(keyValue.getKey(), keyValue.getValue().toString());
        }

        Mono<String> responseMono = request.exchangeToMono(response -> {
            if (response.statusCode().is2xxSuccessful()) {
                return response.bodyToMono(String.class);
            } else if (response.statusCode().is4xxClientError()) {
                return response.bodyToMono(String.class).flatMap(body -> {
                    SafaResponse<String> safaResponse = parseTGenResponse(body, String.class);
                    String error = safaResponse.getBody();
                    return Mono.error(new RuntimeException(error));
                });
            } else {
                return Mono.error(new RuntimeException("HTTP Error " + response.statusCode().value()));
            }
        });

        String responseStr = responseMono.block();
        System.out.println("Response String:" + responseStr);
        return parseTGenResponse(responseStr, requestMeta.responseClass).getBody();
    }

    private <T> T parseResponse(SafaResponse safaResponse, Class<T> targetClass) {
        try {
            if (safaResponse.getStatus() == -1) {
                throw new SafaError("TGen returned with an error.", safaResponse.getBody());
            }
            System.out.println("BODY:" + safaResponse.getBody());
            return objectMapper.readValue(safaResponse.getBody().toString(), targetClass);
        } catch (JsonProcessingException e) {
            throw new SafaError("TGen response not recognized.", e);
        }
    }

    private <T> SafaResponse<T> parseTGenResponse(String body, Class<T> contentClass) {
        try {
            JavaType type = objectMapper.getTypeFactory().constructParametricType(SafaResponse.class, contentClass);
            return objectMapper.readValue(body, type);
        } catch (JsonProcessingException e) {
            throw new SafaError("TGen response not recognized.", e);
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
