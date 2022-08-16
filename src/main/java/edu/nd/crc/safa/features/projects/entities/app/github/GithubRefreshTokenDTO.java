package edu.nd.crc.safa.server.entities.api.github;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Properties representing a GitHub refresh token response for the credentials of
 * a particular user
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class GithubRefreshTokenDTO {

    @JsonProperty("access_token")
    private String accessToken;

    @JsonProperty("refresh_token")
    private String refreshToken;

    @JsonProperty("expires_in")
    private Integer accessTokenExpiration;

    @JsonProperty("refresh_token_expires_in")
    private Integer refreshTokenExpiration;

    private String error;
}
