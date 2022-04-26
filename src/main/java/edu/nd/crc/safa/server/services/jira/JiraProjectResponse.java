package edu.nd.crc.safa.server.services.jira;


import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


/**
 * JIRA api response for the endpoint /project/{id}
 */
@Getter
@Setter
@NoArgsConstructor
public class JiraProjectResponse {

	private String id;
	private String description;
	private String key;
}
