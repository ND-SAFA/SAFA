package edu.nd.crc.safa.server.services.jira;


import java.util.Optional;

import javax.annotation.PostConstruct;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponseDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraRefreshTokenDTO;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.http.codec.json.Jackson2JsonEncoder;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientException;
import reactor.core.publisher.Mono;
import reactor.netty.http.client.HttpClient;


public class JiraConnectionServiceImpl implements JiraConnectionService {

    private static final String ATLASSIAN_API_URL  = "https://api.atlassian.com";
    private static final String ATLASSIAN_AUTH_URL = "https://auth.atlassian.com";
    private static final int API_VERSION = 3;
    private static final String CONTENT_TYPE_HEADER_VALUE = "application/json; charset=UTF-8;";
    private static final String REFRESH_TOKEN_REQUEST_GRANT_TYPE = "refresh_token";
    private final Logger log = LoggerFactory.getLogger(JiraConnectionServiceImpl.class);
    private WebClient apiWebClient;

    private String buildBaseURI(String cloudId) {
        return String.format("/ex/jira/%s/rest/api/%d", cloudId, API_VERSION);
    }

    private String buildApiRequestURI(String cloudId, ApiRoute apiRoute) {
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

    public JiraProjectResponseDTO retrieveJIRAProject(JiraAccessCredentials credentials, Long id) {
        String uri = this.buildApiRequestURI(credentials.getCloudId(), ApiRoute.PROJECT);

        return this.blockOptional(
            this.apiWebClient
                .method(ApiRoute.PROJECT.getMethod())
                .uri(uri, id)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(JiraProjectResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA project"));
    }

    public boolean checkCredentials(JiraAccessCredentials credentials) {
        String uri = this.buildApiRequestURI(credentials.getCloudId(), ApiRoute.MYSELF);

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

    public JiraRefreshTokenDTO refreshAccessToken(JiraAccessCredentials credentials) {
        ObjectMapper mapper = new ObjectMapper();
        JiraRefreshTokenDTO body = JiraRefreshTokenDTO.fromEntity(credentials);

        body.setGrantType(REFRESH_TOKEN_REQUEST_GRANT_TYPE);

        log.info("Initialising jira auth web client");

        return this.blockOptional(
            WebClient.builder()
                .codecs(configure -> {
                    configure.defaultCodecs().enableLoggingRequestDetails(true);
                    configure.defaultCodecs().jackson2JsonEncoder(
                        new Jackson2JsonEncoder(mapper, MediaType.APPLICATION_JSON));
                    configure.defaultCodecs().jackson2JsonDecoder(
                        new Jackson2JsonDecoder(mapper, MediaType.APPLICATION_JSON));
                })
                .clientConnector(new ReactorClientHttpConnector(HttpClient.create()))
                .baseUrl(ATLASSIAN_AUTH_URL)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, CONTENT_TYPE_HEADER_VALUE)
                .build()
                .method(ApiRoute.REFRESH_TOKEN.getMethod())
                .uri(ApiRoute.REFRESH_TOKEN.getPath())
                .bodyValue(body)
                .retrieve()
                .bodyToMono(JiraRefreshTokenDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to refresh JIRA credentials"));
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
        MYSELF("/myself", HttpMethod.GET),
        REFRESH_TOKEN("/oauth/token", HttpMethod.POST);

        private final String path;

        private final HttpMethod method;
    }
}

