package edu.nd.crc.safa.server.services.jira;


import javax.persistence.Column;

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

	@JsonProperty("access_token")
	private String accessToken;

	@JsonProperty("client_secret")
	private String clientSecret;

	@JsonProperty("client_id")
	private String clientId;

	@JsonProperty("refresh_token")
	private String refreshToken;

	public static JiraRefreshTokenDTO fromEntity(JiraAccessCredentials credentials) {
		JiraRefreshTokenDTO dto = new JiraRefreshTokenDTO();

		dto.setAccessToken(new String(credentials.getBearerAccessToken()));
		dto.setClientId(credentials.getClientId());
		dto.setClientSecret(credentials.getClientSecret());
		dto.setRefreshToken(credentials.getRefreshToken());
		return dto;
	}
}
