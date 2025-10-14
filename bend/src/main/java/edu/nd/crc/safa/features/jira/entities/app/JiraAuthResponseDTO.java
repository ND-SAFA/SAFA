package edu.nd.crc.safa.features.jira.entities.app;

import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;


/**
* POJO to be used as body payload and response when accessing auth endpoints
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraAuthResponseDTO {
    /**
     * READ_ONLY since we are only interested in sending this field, not receiving it
     */
    @JsonProperty(value = "grant_type", access = JsonProperty.Access.READ_ONLY)
    private String grantType;

    /**
     * WRITE_ONLY since we are only interested in receiving this field, not sending it
     */
    @JsonProperty(value = "access_token", access = JsonProperty.Access.WRITE_ONLY)
    private String accessToken;

    @JsonProperty("client_secret")
    private String clientSecret;

    @JsonProperty("client_id")
    private String clientId;

    @JsonProperty("refresh_token")
    private String refreshToken;

    public static JiraAuthResponseDTO fromEntity(JiraAccessCredentials credentials) {
        JiraAuthResponseDTO dto = new JiraAuthResponseDTO();

        dto.setClientId(credentials.getClientId());
        dto.setClientSecret(credentials.getClientSecret());
        dto.setRefreshToken(credentials.getRefreshToken());
        return dto;
    }
}
