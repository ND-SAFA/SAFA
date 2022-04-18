package edu.nd.crc.safa.server.entities.api;

/**
 * Describes the information needed to import a project from JIRA.
 */
public class JIRAProjectPullRequest {

    String cloudId; // The domain resource id
    String projectId; // The project id within domain
    String bearerAccessToken; // The user authentication id
    String clientSecret; // used for refreshing the token later

    public JIRAProjectPullRequest() {
    }

    public String getCloudId() {
        return cloudId;
    }

    public void setCloudId(String cloudId) {
        this.cloudId = cloudId;
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getBearerAccessToken() {
        return bearerAccessToken;
    }

    public void setBearerAccessToken(String bearerAccessToken) {
        this.bearerAccessToken = bearerAccessToken;
    }

    public String getClientSecret() {
        return clientSecret;
    }

    public void setClientSecret(String clientSecret) {
        this.clientSecret = clientSecret;
=    }
}
