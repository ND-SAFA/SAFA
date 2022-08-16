package edu.nd.crc.safa.server.entities.api.github;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;

import lombok.Data;

/**
 * Describes the information needed to import a GitHub project
 */
@Data
public class GithubAccessCredentialsDTO {

    /**
     * The user authentication id
     */
    @NotNull
    @NotEmpty(message = "Access token secret cannot be empty")
    private String accessToken;

    /**
     * Client secret
     */
    @NotNull
    @NotEmpty(message = "Client secret cannot be empty")
    private String clientSecret;

    /**
     * Client id
     */
    @NotNull
    @NotEmpty(message = "Client id cannot be empty")
    private String clientId;

    /**
     * Refresh token
     */
    @NotNull
    @NotEmpty(message = "Refresh token cannot be empty")
    private String refreshToken;

    /**
     * In how many minutes the access token will expire
     */
    @NotNull
    private Integer accessTokenExpiration;

    /**
     * In how many minutes the refresh token will expire
     */
    @NotNull
    private Integer refreshTokenExpiration;

    public GithubAccessCredentials toEntity() {
        GithubAccessCredentials entity = new GithubAccessCredentials();

        entity.setAccessToken(this.getAccessToken());
        entity.setClientId(this.getClientId());
        entity.setClientSecret(this.getClientSecret());
        entity.setRefreshToken(this.getRefreshToken());
        entity.setAccessTokenExpiration(this.getAccessTokenExpiration());
        entity.setRefreshTokenExpiration(this.getRefreshTokenExpiration());

        return entity;
    }
}
