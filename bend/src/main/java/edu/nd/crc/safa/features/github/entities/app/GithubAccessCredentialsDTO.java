package edu.nd.crc.safa.features.github.entities.app;

import java.util.Objects;

import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Describes the information needed to import a GitHub project
 */
@Data
public class GithubAccessCredentialsDTO {

    /**
     * The user authentication id
     */
    @JsonProperty("access_token")
    private String accessToken;

    /**
     * Client secret
     */
    @JsonProperty("client_secret")
    private String clientSecret;

    /**
     * Client id
     */
    @JsonProperty("client_id")
    private String clientId;

    private String error;

    @JsonProperty("error_description")
    private String errorDescription;

    @JsonProperty("error_uri")
    private String errorUri;

    public boolean isError() {
        return !Objects.isNull(this.error);
    }

    public GithubAccessCredentials toEntity() {
        GithubAccessCredentials entity = new GithubAccessCredentials();

        entity.setAccessToken(this.getAccessToken());
        entity.setClientId(this.getClientId());
        entity.setClientSecret(this.getClientSecret());

        return entity;
    }
}
