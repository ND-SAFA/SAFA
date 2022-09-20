package edu.nd.crc.safa.features.jira.entities.app;

import java.util.HashMap;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * DTO encapsulating data retrieved when checking project permissions
 */
@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class JiraProjectPermissionDTO {

    public static final String ADMINISTER_PROJECTS_PERMISSION = "ADMINISTER_PROJECTS";

    private HashMap<String, Permission> permissions = new HashMap<>();

    @Data
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class Permission {
        String description;
        Boolean havePermission;
        Long id;
        String key;
        String name;
        String type;
    }
}
