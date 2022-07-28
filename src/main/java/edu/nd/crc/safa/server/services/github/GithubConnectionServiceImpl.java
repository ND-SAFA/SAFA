package edu.nd.crc.safa.server.services.github;


import edu.nd.crc.safa.config.WebApiConfiguration;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.github.*;
import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.utilities.WebApiUtils;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriBuilder;

import java.util.List;

@AllArgsConstructor
public class GithubConnectionServiceImpl implements GithubConnectionService {

    private static final String GITHUB_API_URL = "https://api.github.com";
    private static final String GITHUB_AUTH_URL = "https://github.com/login/oauth";
    private static final String REFRESH_TOKEN_REQUEST_GRANT_TYPE = "refresh_token";

    private static final String CLIENT_ID_PARAM = "client_id";
    private static final String CLIENT_SECRET_PARAM = "client_secret";
    private static final String REFRESH_TOKEN_PARAM = "refresh_token";
    private static final String GRANT_TYPE_PARAM = "grant_type";

    private static final String REPOSITORIES_SORT_PARAM = "sort";
    private static final String REPOSITORIES_SORT_DIR_PARAM = "direction";
    private static final String REPOSITORIES_AFFILIATION_PARAM = "affiliation";
    private static final String REPOSITORIES_PAGE_SIZE_PARAM = "per_page";

    private static final String FILETREE_RECURSIVE_PARAM = "recursive";

    private final WebClient webClient;

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
    public GithubRefreshTokenDTO refreshAccessToken(GithubAccessCredentials credentials) {
        return WebApiUtils.blockOptional(
            this.webClient
                    .method(ApiRoute.REFRESH_TOKEN.getMethod())
                    .uri(ApiRoute.REFRESH_TOKEN.getFullPath(), builder ->
                        this.setAuthorizationQueryParameters(builder, credentials)
                            .queryParam(GRANT_TYPE_PARAM, REFRESH_TOKEN_REQUEST_GRANT_TYPE)
                            .build()
                    )
                    .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                    .retrieve()
                    .bodyToMono(GithubRefreshTokenDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to refresh GitHub credentials"));
    }

    @Override
    public List<GithubRepositoryDTO> getUserRepositories(GithubAccessCredentials credentials) {
        return WebApiUtils.blockOptional(
                this.webClient
                        .method(ApiRoute.REPOSITORIES.getMethod())
                        .uri(ApiRoute.REPOSITORIES.getFullPath(), builder ->
                            builder
                                .queryParam(REPOSITORIES_SORT_PARAM, "updated")
                                .queryParam(REPOSITORIES_SORT_DIR_PARAM, "desc")
                                .queryParam(REPOSITORIES_AFFILIATION_PARAM,
                                        "owner,collaborator,organization_member")
                                .queryParam(REPOSITORIES_PAGE_SIZE_PARAM, 100)
                                .build()
                        )
                        .header(HttpHeaders.AUTHORIZATION,
                                this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                        .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                        .retrieve()
                        .bodyToMono(new ParameterizedTypeReference<List<GithubRepositoryDTO>>() {
                        })
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve repositories"));
    }

    @Override
    public List<GithubRepositoryBranchDTO> getRepositoryBranches(GithubAccessCredentials credentials,
                                                                 String repositoryName) {
        return WebApiUtils.blockOptional(
                this.webClient
                        .method(ApiRoute.REPOSITORY_BRANCHES.getMethod())
                        .uri(ApiRoute.REPOSITORY_BRANCHES.getFullPath(),
                                credentials.getGithubHandler(), repositoryName
                        )
                        .header(HttpHeaders.AUTHORIZATION,
                                this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                        .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                        .retrieve()
                        .bodyToMono(new ParameterizedTypeReference<List<GithubRepositoryBranchDTO>>() {
                        })
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve repository branches for " + repositoryName));
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
        .map(GithubRepositoryFiletreeResponseDTO::filterOutFolders)
        .orElseThrow(() -> new SafaError("Error while trying to retrieve file tree for " + repositoryName));
    }

    @Override
    public GithubCommitDiffResponseDTO getDiffBetweenOldCommitAndHead(GithubAccessCredentials credentials,
                                                                      String repositoryName,
                                                                      String baseCommitSha) {
        String commitRange = String.format("%s...HEAD", baseCommitSha);

        return WebApiUtils.blockOptional(
                this.webClient
                        .method(ApiRoute.COMMIT_DIFF.getMethod())
                        .uri(ApiRoute.COMMIT_DIFF.getFullPath(),
                                credentials.getGithubHandler(), repositoryName, commitRange
                        )
                        .header(HttpHeaders.AUTHORIZATION,
                                this.buildAuthorizationHeaderValue(credentials.getAccessToken()))
                        .header(HttpHeaders.ACCEPT, WebApiConfiguration.JSON_CONTENT_TYPE_HEADER_VALUE)
                        .retrieve()
                        .bodyToMono(GithubCommitDiffResponseDTO.class)
        ).orElseThrow(() -> new SafaError("Error while trying to retrieve diff starting from " + baseCommitSha));
    }

    private String buildAuthorizationHeaderValue(String token) {
        return String.format("token %s", token);
    }

    private UriBuilder setAuthorizationQueryParameters(UriBuilder builder, GithubAccessCredentials credentials) {

        return builder
                .queryParam(CLIENT_ID_PARAM, credentials.getClientId())
                .queryParam(CLIENT_SECRET_PARAM, credentials.getClientSecret())
                .queryParam(REFRESH_TOKEN_PARAM, credentials.getRefreshToken());
    }

    @Getter
    @AllArgsConstructor
    private enum ApiRoute {
        REFRESH_TOKEN(GITHUB_AUTH_URL, "/access_token", HttpMethod.POST),
        USER(GITHUB_API_URL, "/user", HttpMethod.GET),
        REPOSITORIES(GITHUB_API_URL, "/user/repos", HttpMethod.GET),
        REPOSITORY_BRANCHES(GITHUB_API_URL, "/repos/{username}/{repo}/branches", HttpMethod.GET),
        REPOSITORY_FILETREE(GITHUB_API_URL, "/repos/{username}/{repo}/git/trees/{sha}", HttpMethod.GET),
        COMMIT_DIFF(GITHUB_API_URL, "/repos/{username}/{repo}/compare/{basehead}", HttpMethod.GET);

        private final String url;

        private final String path;

        private final HttpMethod method;

        public String getFullPath() {
            return url + path;
        }
    }
}
