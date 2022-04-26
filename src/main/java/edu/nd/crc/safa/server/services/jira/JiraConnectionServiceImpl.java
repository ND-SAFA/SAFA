package edu.nd.crc.safa.server.services.jira;

import java.util.Optional;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponse;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientException;
import reactor.core.publisher.Mono;

public class JiraConnectionServiceImpl implements JiraConnectionService {

    private static final String ATLASSIAN_API_URL = "https://api.atlassian.com/ex";
    private static final String ATLASSIAN_AUTH_URL = "https://auth.atlassian.com/oauth/token";
    private static final int API_VERSION = 3;
    private static final String CONTENT_TYPE_HEADER_VALUE = "application/json; charset=UTF-8;";
    private final Logger log = LoggerFactory.getLogger(JiraConnectionServiceImpl.class);
    private WebClient apiWebClient;

    private String buildBaseURI(String cloudId) {
        return String.format("/jira/%s/rest/api/%d", cloudId, API_VERSION);
    }

    private String buildRequestURI(String cloudId, ApiRoute apiRoute) {
        return this.buildBaseURI(cloudId) + apiRoute.getPath();
    }

    private String buildAuthorizationHeaderValue(byte[] token) {
        return String.format("Bearer %s", new String(token));
    }

    @PostConstruct
    private void init() {
        this.apiWebClient = WebClient.builder()
            .baseUrl(ATLASSIAN_API_URL)
            .defaultHeader(HttpHeaders.CONTENT_TYPE, CONTENT_TYPE_HEADER_VALUE)
            .build();

        log.info("Web client initialised");
    }

    public JiraProjectResponse retrieveJIRAProject(JiraAccessCredentials credentials, Long id) {
        String uri = this.buildRequestURI(credentials.getCloudId(), ApiRoute.PROJECT);

        return this.blockOptional(
            this.apiWebClient
                .method(ApiRoute.PROJECT.getMethod())
                .uri(uri, id)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(JiraProjectResponse.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA project"));
    }

    public boolean checkCredentials(JiraAccessCredentials credentials) {
        String uri = this.buildRequestURI(credentials.getCloudId(), ApiRoute.MYSELF);

        HttpStatus code = this.blockOptional(
            this.apiWebClient
                .method(ApiRoute.MYSELF.getMethod())
                .uri(uri)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .toBodilessEntity()
                .map(ResponseEntity::getStatusCode)
        ).orElseGet(() -> HttpStatus.BAD_REQUEST);

        return HttpStatus.OK.equals(code);
    }

    public JiraAccessCredentials refreshAccessToken(JiraAccessCredentials credentials) {
        throw new UnsupportedOperationException("Work in progress");
    }

    private <T> Optional<T> blockOptional(Mono<T> mono) {
        try {
            return mono.blockOptional();
        } catch (WebClientException ex) {
            log.error("Exception thrown while executing blocking call", ex);
            throw new SafaError("Exception thrown while executing blocking call", ex);
        }
    }

    @Getter
    @AllArgsConstructor
    private enum ApiRoute {
        PROJECT("/project/{id}", HttpMethod.GET),
        MYSELF("/myself", HttpMethod.GET);

        private final String path;

        private final HttpMethod method;
    }
}

