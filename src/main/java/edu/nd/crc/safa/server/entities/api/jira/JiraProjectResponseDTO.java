package edu.nd.crc.safa.server.entities.api.jira;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;


/**
 * JIRA api response for the endpoint /project/{id}
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraProjectResponseDTO {

    String id;
    String description;
    String key;
    String name;
    Boolean isPrivate;
    String style;

}
