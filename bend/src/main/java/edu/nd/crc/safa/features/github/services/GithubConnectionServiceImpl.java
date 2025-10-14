package edu.nd.crc.safa.features.github.services;

import java.util.Optional;

import edu.nd.crc.safa.config.WebApiConfiguration;
import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubFileBlobDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryFiletreeResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.WebApiUtils;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriBuilder;

public class GithubConnectionServiceImpl implements GithubConnectionService {

    private static final String GITHUB_API_URL = "https://api.github.com";
    private static final String GITHUB_AUTH_URL = "https://github.com/login/oauth";

    private static final String CLIENT_ID_PARAM = "client_id";
    private static final String CLIENT_SECRET_PARAM = "client_secret";

    private static final String ACCESS_CODE_PARAM = "code";

    private static final String FILETREE_RECURSIVE_PARAM = "recursive";

    private final WebClient webClient;

    private final GithubAccessCredentialsRepository accessCredentialsRepository;

    @Value("${integrations.github.client-id}")
    private String clientId;

    @Value("${integrations.github.client-secret}")
    private String clientSecret;

    public GithubConnectionServiceImpl(WebClient webClient,
                                       GithubAccessCredentialsRepository accessCredentialsRepository) {
        this.webClient = webClient;
        this.accessCredentialsRepository = accessCredentialsRepository;
    }

    @Override
    public Optional<GithubAccessCredentials> getGithubCredentials(SafaUser user) {
        Optional<GithubAccessCredentials> credentials = accessCredentialsRepository.findByUser(user);
        credentials.ifPresent(cred -> {
            cred.setClientId(clientId);
            cred.setClientSecret(clientSecret);
        });
        return credentials;
    }

    @Override
    public void deleteGithubCredentials(SafaUser user) {
        Optional<GithubAccessCredentials> credentials = accessCredentialsRepository.findByUser(user);
        credentials.ifPresent(accessCredentialsRepository::delete);
    }

    @Override
    public GithubSelfResponseDTO getSelf(GithubAccessCredentials credentials) {
        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.USER.getMethod())
                .uri(ApiRoute.USER.getFullPath())
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                .retrieve()
                .bodyToMono(GithubSelfResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to refresh GitHub credentials"));
    }

    @Override
    public GithubRepositoryFiletreeResponseDTO getRepositoryFiles(GithubAccessCredentials credentials,
                                                                  String repositoryName,
                                                                  String commitSha) {
        return WebApiUtils.blockOptional(
                this.webClient
                    .method(ApiRoute.REPOSITORY_FILETREE.getMethod())
                    .uri(ApiRoute.REPOSITORY_FILETREE.getFullPath(), builder ->
                        builder
                            .queryParam(FILETREE_RECURSIVE_PARAM, true)
                            .build(credentials.getGithubHandler(), repositoryName, commitSha)
                    )
                    .header(HttpHeaders.AUTHORIZATION,
                        this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                    .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                    .retrieve()
                    .bodyToMono(GithubRepositoryFiletreeResponseDTO.class)
            )
            .map(GithubRepositoryFiletreeResponseDTO::filesOnly)
            .orElseThrow(() -> new SafaError("Error while trying to retrieve file tree for " + repositoryName));
    }

    @Override
    public GithubCommitDiffResponseDTO getDiffBetweenOldCommitAndHead(GithubAccessCredentials credentials,
                                                                      String repositoryOwner,
                                                                      String repositoryName,
                                                                      String baseCommitSha,
                                                                      String branchName) {
        String commitRange = String.format("%s...%s", baseCommitSha, branchName);

        return WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.COMMIT_DIFF.getMethod())
                .uri(ApiRoute.COMMIT_DIFF.getFullPath(),
                    repositoryOwner, repositoryName, commitRange
                )
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                .retrieve()
                .bodyToMono(GithubCommitDiffResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve diff starting from " + baseCommitSha));
    }

    @Override
    public GithubFileBlobDTO getBlobInformation(GithubAccessCredentials credentials, String url) {
        return WebApiUtils.blockOptional(
            this.webClient
                .method(HttpMethod.GET)
                .uri(url)
                .header(HttpHeaders.AUTHORIZATION,
                    this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                .retrieve()
                .bodyToMono(GithubFileBlobDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve blob information from " + url));
    }

    @Override
    public GithubAccessCredentialsDTO useAccessCode(String accessCode) {
        GithubAccessCredentialsDTO dto = WebApiUtils.blockOptional(
            this.webClient
                .method(ApiRoute.ACCESS_CODE.getMethod())
                .uri(ApiRoute.ACCESS_CODE.getFullPath(), builder ->
                    this.setAuthorizationQueryParameters(builder, clientId, clientSecret)
                        .queryParam(ACCESS_CODE_PARAM, accessCode)
                        .build()
                )
                .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                .headers(headers -> {
                    // Apparently the GitHub API doesn't like this particular header on this
                    // particular endpoint
                    headers.remove(HttpHeaders.CONTENT_TYPE);
                })
                .retrieve()
                .bodyToMono(GithubAccessCredentialsDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve access token"));

        dto.setClientId(this.clientId);
        dto.setClientSecret(this.clientSecret);
        return dto;
    }

    private String buildAuthorizationHeaderValue(String token) {
        return String.format("token %s", token);
    }

    private UriBuilder setAuthorizationQueryParameters(UriBuilder builder, String clientId, String clientSecret) {
        return builder
            .queryParam(CLIENT_ID_PARAM, clientId)
            .queryParam(CLIENT_SECRET_PARAM, clientSecret);
    }

    @Getter
    @AllArgsConstructor
    private enum ApiRoute {
        REFRESH_TOKEN(GITHUB_AUTH_URL, "/access_token", HttpMethod.POST),
        USER(GITHUB_API_URL, "/user", HttpMethod.GET),
        REPOSITORIES(GITHUB_API_URL, "/user/repos", HttpMethod.GET),
        SINGLE_REPOSITORY(GITHUB_API_URL, "/repos/{username}/{repository_name}", HttpMethod.GET),
        REPOSITORY_BRANCHES(GITHUB_API_URL, "/repos/{username}/{repo}/branches", HttpMethod.GET),
        SINGLE_REPOSITORY_BRANCH(GITHUB_API_URL, "/repos/{username}/{repo}/branches/{branch}", HttpMethod.GET),
        REPOSITORY_FILETREE(GITHUB_API_URL, "/repos/{username}/{repo}/git/trees/{sha}", HttpMethod.GET),
        COMMIT_DIFF(GITHUB_API_URL, "/repos/{username}/{repo}/compare/{basehead}", HttpMethod.GET),
        ACCESS_CODE(GITHUB_AUTH_URL, "/access_token", HttpMethod.POST);

        private final String url;

        private final String path;

        private final HttpMethod method;

        public String getFullPath() {
            return url + path;
        }
    }
}
