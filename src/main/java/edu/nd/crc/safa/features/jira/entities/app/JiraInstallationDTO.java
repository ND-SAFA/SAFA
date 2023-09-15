package edu.nd.crc.safa.features.jira.entities.app;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * DTO mapping information about a JIRA installation
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraInstallationDTO {

    private String id;
    private String name;
    private String avatarUrl;
    private List<String> scopes = new ArrayList<>();
}
