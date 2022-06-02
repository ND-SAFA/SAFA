package edu.nd.crc.safa.server.entities.api.jira;

import lombok.Data;


/**
 * JIRA api response for the endpoint /project/{id}
 */
@Data
public class JiraProjectResponseDTO {

    String id;
    String description;
    String key;
    String name;
    Boolean isPrivate;
    String style;

}
