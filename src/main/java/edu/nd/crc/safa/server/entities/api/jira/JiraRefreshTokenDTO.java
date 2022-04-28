package edu.nd.crc.safa.server.entities.api.jira;

import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


/**
 * POJO to be used as body payload and response when refreshing current credentials
 */
@Getter
@Setter
@NoArgsConstructor
public class JiraRefreshTokenDTO {

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

    public static JiraRefreshTokenDTO fromEntity(JiraAccessCredentials credentials) {
        JiraRefreshTokenDTO dto = new JiraRefreshTokenDTO();

        dto.setClientId(credentials.getClientId());
        dto.setClientSecret(credentials.getClientSecret());
        dto.setRefreshToken(credentials.getRefreshToken());
        return dto;
    }
}
