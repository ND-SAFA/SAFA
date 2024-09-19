package edu.nd.crc.safa.features.jira.services;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.jira.entities.app.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraAuthResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraCredentialsRequestBodyDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectPermissionDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.WebApiUtils;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.client.WebClient;

public class JiraConnectionServiceImpl implements JiraConnectionService {

    private static final String ATLASSIAN_API_URL = "https://api.atlassian.com";
    private static final String ATLASSIAN_AUTH_URL = "https://auth.atlassian.com";
    private static final int API_VERSION = 3;
    private static final String REFRESH_TOKEN_REQUEST_GRANT_TYPE = "refresh_token";
    private static final String ACCESS_CODE_REQUEST_GRANT_TYPE = "authorization_code";
    private static final Logger log = LoggerFactory.getLogger(JiraConnectionServiceImpl.class);

    private static final String JIRA_ISSUE_UPDATE_DATE_FORMAT = "yyyy-MM-dd HH:mm";

    private final JiraAccessCredentialsRepository accessCredentialsRepository;

    private final WebClient webClient;

    @Value("${integrations.jira.client-id}")
    private String clientId;

    @Value("${integrations.jira.client-secret}")
    private String clientSecret;

    @Value("${integrations.jira.redirect-link}")
    private String redirectLink;

    public JiraConnectionServiceImpl(JiraAccessCredentialsRepository accessCredentialsRepository, WebClient webClient) {
        this.webClient = webClient;
        this.accessCredentialsRepository = accessCredentialsRepository;
    }

    public Optional<JiraAccessCredentials> getJiraCredentials(SafaUser user) {
        Optional<JiraAccessCredentials> credentials = accessCredentialsRepository.findByUser(user);
        credentials.ifPresent(cred -> {
            cred.setClientId(clientId);
            cred.setClientSecret(clientSecret);
        });
        return credentials;
    }

    private String buildBaseURI(UUID orgId) {
        return String.format("/ex/jira/%s/rest/api/%d", orgId, API_VERSION);
    }

    private String buildApiRequestURI(UUID orgId, ApiRoute apiRoute) {
        return apiRoute.getUrl() + this.buildBaseURI(orgId) + apiRoute.getPath();
    }

    private String buildAuthRequestURI(ApiRoute apiRoute) {
        return apiRoute.getUrl() + apiRoute.getPath();
    }

    private String buildAuthorizationHeaderValue(byte[] token) {
        return String.format("Bearer %s", new String(token));
    }

    @Override
    public JiraProjectResponseDTO retrieveJIRAProject(JiraAccessCredentials credentials,
                                                      UUID orgId, Long jiraProjectId) {

        String uri = this.buildApiRequestURI(orgId, ApiRoute.PROJECT);

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.PROJECT.getMethod())
                .uri(uri, jiraProjectId)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(JiraProjectResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA project"));
    }

    public boolean checkCredentials(JiraAccessCredentials credentials) {
        try {
            getInstallations(credentials);
            return true;
        } catch (SafaError e) {
            return false;
        }
    }

    public JiraAuthResponseDTO refreshAccessToken(JiraAccessCredentials credentials) {
        String uri = this.buildAuthRequestURI(ApiRoute.REFRESH_TOKEN);
        JiraAuthResponseDTO body = JiraAuthResponseDTO.fromEntity(credentials);

        body.setGrantType(REFRESH_TOKEN_REQUEST_GRANT_TYPE);

        log.info("Initialising jira auth web client");

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.REFRESH_TOKEN.getMethod())
                .uri(uri)
                .bodyValue(body)
                .retrieve()
                .bodyToMono(JiraAuthResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to refresh JIRA credentials"));
    }

    @Override
    public List<JiraProjectResponseDTO> retrieveJIRAProjectsPreview(JiraAccessCredentials credentials, UUID orgId) {
        String uri = this.buildApiRequestURI(orgId, ApiRoute.PROJECTS_PREVIEW);

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.PROJECTS_PREVIEW.getMethod())
                .uri(uri)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<JiraProjectResponseDTO>>() {
                })
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA project"));
    }

    @Override
    public List<JiraIssueDTO> retrieveJIRAIssues(JiraAccessCredentials credentials,
                                                 UUID orgId, Long jiraProjectId) {

        String jqlQuery = String.format("project=%s", jiraProjectId);

        return this.getJIRAIssues(credentials, orgId, jqlQuery);
    }

    @Override
    public List<JiraIssueDTO> retrieveUpdatedJIRAIssues(JiraAccessCredentials credentials,
                                                        UUID orgId,
                                                        Long jiraProjectId,
                                                        Date timestamp) {

        String updateDate = new SimpleDateFormat(JIRA_ISSUE_UPDATE_DATE_FORMAT).format(timestamp);
        String jqlQuery = String.format(
            "project=%s AND (updated>\"%s\" OR created>\"%s\")", jiraProjectId, updateDate, updateDate);

        return this.getJIRAIssues(credentials, orgId, jqlQuery);
    }

    @Override
    public boolean checkUserCanViewProjectIssues(JiraAccessCredentials credentials,
                                                 UUID orgId, Long jiraProjectId) {

        String uri = this.buildApiRequestURI(orgId, ApiRoute.PERMISSIONS);

        JiraProjectPermissionDTO permissionDTO = WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.PERMISSIONS.getMethod())
                .uri(uri, builder ->
                    builder
                        .queryParam("permissions", JiraProjectPermissionDTO.BROWSE_PROJECTS_PERMISSION)
                        .queryParam("projectId", jiraProjectId)
                        .build()
                ).header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(JiraProjectPermissionDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve JIRA permission"));

        if (!permissionDTO.getPermissions().containsKey(JiraProjectPermissionDTO.BROWSE_PROJECTS_PERMISSION)) {
            return false;
        }

        return permissionDTO.getPermissions()
            .get(JiraProjectPermissionDTO.BROWSE_PROJECTS_PERMISSION).getHavePermission();
    }

    @Override
    public JiraAccessCredentialsDTO useAccessCode(String accessCode) {
        String uri = this.buildAuthRequestURI(ApiRoute.REFRESH_TOKEN);
        JiraCredentialsRequestBodyDTO body = new JiraCredentialsRequestBodyDTO();

        body.setCode(accessCode);
        body.setGrantType(ACCESS_CODE_REQUEST_GRANT_TYPE);
        body.setClientId(this.clientId);
        body.setClientSecret(this.clientSecret);
        body.setRedirectLink(this.redirectLink);

        JiraAuthResponseDTO dto = WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.REFRESH_TOKEN.getMethod())
                .uri(uri)
                .bodyValue(body)
                .retrieve()
                .bodyToMono(JiraAuthResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to use access code"));

        JiraAccessCredentialsDTO result = new JiraAccessCredentialsDTO();

        result.setBearerAccessToken(dto.getAccessToken());
        result.setClientId(clientId);
        result.setClientSecret(clientSecret);
        result.setRefreshToken(dto.getRefreshToken());
        return result;
    }

    @Override
    public List<JiraInstallationDTO> getInstallations(JiraAccessCredentials credentials) {
        String uri = this.buildAuthRequestURI(ApiRoute.INSTALLATIONS);

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.INSTALLATIONS.getMethod())
                .uri(uri)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(new ParameterizedTypeReference<List<JiraInstallationDTO>>() {
                })
        ).orElseThrow(() -> new SafaError("Error while trying to use access code"));
    }

    public List<JiraIssueDTO> getJIRAIssues(JiraAccessCredentials credentials, UUID orgId, String jqlQuery) {
        JiraIssuesResponseDTO response = getJIRAIssuesStartingAt(credentials, orgId, jqlQuery, 0);
        List<JiraIssueDTO> issues = response.getIssues();
        int totalIssues = response.getTotal();

        while (issues.size() < totalIssues) {
            response = getJIRAIssuesStartingAt(credentials, orgId, jqlQuery, issues.size());
            issues.addAll(response.getIssues());
        }

        return issues;
    }

    private JiraIssuesResponseDTO getJIRAIssuesStartingAt(JiraAccessCredentials credentials, UUID orgId,
                                                          String jqlQuery, int startingAt) {
        String baseUri = this.buildApiRequestURI(orgId, ApiRoute.ISSUES);

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.ISSUES.getMethod())
                .uri(baseUri, builder ->
                    builder
                        .queryParam("jql", jqlQuery)
                        .queryParam("startAt", startingAt)
                        .queryParam("fields")
                        .build()
                )
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getBearerAccessToken()))
                .retrieve()
                .bodyToMono(JiraIssuesResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to refresh JIRA credentials"));
    }

    @Getter
    @AllArgsConstructor
    private enum ApiRoute {
        PROJECT(ATLASSIAN_API_URL, "/project/{id}", HttpMethod.GET),
        PROJECTS_PREVIEW(ATLASSIAN_API_URL, "/project", HttpMethod.GET),
        REFRESH_TOKEN(ATLASSIAN_AUTH_URL, "/oauth/token", HttpMethod.POST),
        ISSUES(ATLASSIAN_API_URL, "/search", HttpMethod.GET),
        PERMISSIONS(ATLASSIAN_API_URL, "/mypermissions", HttpMethod.GET),
        ACCESS_CODE(ATLASSIAN_AUTH_URL, "/oauth/token", HttpMethod.POST),
        INSTALLATIONS(ATLASSIAN_API_URL, "/oauth/token/accessible-resources", HttpMethod.GET);

        private final String url;

        private final String path;

        private final HttpMethod method;
    }
}

