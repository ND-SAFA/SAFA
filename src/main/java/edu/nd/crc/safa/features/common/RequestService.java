package edu.nd.crc.safa.features.common;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * Builds and performs HTTP/HTTPS requests.
 */
@AllArgsConstructor
@Service
public class RequestService {
    private static final Logger logger = LoggerFactory.getLogger(RequestService.class);
    private final ObjectMapper objectMapper = ObjectMapperConfig.create();
    private final int DEFAULT_TIMEOUT = 60 * 60; // 1 Hour
    private final RestTemplate restTemplate;

    /**
     * Performs a POST request.
     *
     * @param endpoint      Where to send request to.
     * @param payload       The payload to send in body of request.
     * @param cookies       Cookies to add to request.
     * @param responseClass The expected class response should be in.
     * @param <T>           The type associated with response to parse.
     * @return The parsed of generic type.
     */
    public <T> T sendPost(String endpoint,
                          Object payload,
                          Map<String, String> cookies,
                          Class<T> responseClass) {
        // Step - Send request
        return sendPayload(endpoint, payload, cookies, responseClass, HttpMethod.POST);
    }

    /**
     * Performs request with JSON headers.
     *
     * @param endpoint      The endpoint to send request to.
     * @param payload       The payload to send in request.
     * @param cookies       Cookies to add to request.
     * @param responseClass The expected class to parse response to.
     * @param method        The type of HTTP method to make request with.
     * @param <T>           The generic type to parse response to.
     * @return The parsed response.
     */
    public <T> T sendPayload(String endpoint,
                             Object payload,
                             Map<String, String> cookies,
                             Class<T> responseClass,
                             HttpMethod method) {
        String requestLog = String.format("Starting request to %s", endpoint);
        logger.debug(requestLog);

        HttpHeaders headers = new HttpHeaders();
        headers.setAccept(List.of(MediaType.APPLICATION_JSON));

        if (cookies != null && !cookies.isEmpty()) {
            headers.set(HttpHeaders.COOKIE, buildCookieString(cookies));
        }

        HttpEntity<Object> headerEntity = new HttpEntity<>(payload, headers);

        ResponseEntity<String> response = restTemplate.exchange(endpoint, method, headerEntity, String.class);
        String responseBody = response.getBody();

        if (responseBody == null) {
            logger.warn("Null body received in response to request to {}\nstatus code: {}",
                endpoint, response.getStatusCode());
            responseBody = String.format("%s %s", response.getStatusCode(), endpoint);
        }

        if (JsonFileUtilities.isValid(responseBody)) {
            return JsonFileUtilities.parse(responseBody, responseClass);
        } else {
            String error = String.format("Error occurred @ %s %s", method, endpoint);
            logger.error(error);
            throw new SafaError(responseBody);
        }
    }

    /**
     * Builds the cookie string from a map of cookie name-value pairs.
     *
     * @param cookies Map containing cookie name-value pairs.
     * @return String representing the cookie string.
     */
    private String buildCookieString(Map<String, String> cookies) {
        StringBuilder cookieBuilder = new StringBuilder();
        cookies.forEach((name, value) -> cookieBuilder.append(name).append("=").append(value).append("; "));
        return cookieBuilder.toString();
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
