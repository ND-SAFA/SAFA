package edu.nd.crc.safa.features.jira.entities.app;

import java.nio.charset.StandardCharsets;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;

import lombok.Data;

/**
 * Describes the information needed to import a project from JIRA.
 */
@Data
public class JiraAccessCredentialsDTO {

    /**
     * The domain resource id
     */
    @NotNull
    private String cloudId;

    /**
     * The user authentication id
     */
    @NotNull
    private String bearerAccessToken;

    /**
     * Client secret
     */
    @NotNull
    private String clientSecret;

    /**
     * Client id
     */
    @NotNull
    private String clientId;

    /**
     * Refresh token
     */
    @NotNull
    private String refreshToken;

    public JiraAccessCredentials toEntity() {
        JiraAccessCredentials entity = new JiraAccessCredentials();

        entity.setBearerAccessToken(this.getBearerAccessToken().getBytes(StandardCharsets.UTF_8));
        entity.setClientId(this.getClientId());
        entity.setClientSecret(this.getClientSecret());
        entity.setCloudId(this.getCloudId());
        entity.setRefreshToken(this.getRefreshToken());

        return entity;
    }
}
