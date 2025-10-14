package edu.nd.crc.safa.features.jira.entities.app;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * Plain Java Object representing the request body sent when trying to use a JIRA access code
 */
@Data
public class JiraCredentialsRequestBodyDTO {

    private String code;

    @JsonProperty("grant_type")
    private String grantType;

    @JsonProperty("client_id")
    private String clientId;

    @JsonProperty("client_secret")
    private String clientSecret;

    @JsonProperty("redirect_uri")
    private String redirectLink;
}
