package edu.nd.crc.safa.features.jira.entities.api;

import java.util.UUID;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Information for identifying jira project.
 */
@Data
@AllArgsConstructor
public class JiraIdentifier {
    /**
     * The project version identified by this JIRA project.
     */
    private ProjectVersion projectVersion;
    /**
     * The JIRA id of the project.
     */
    private Long jiraProjectId;
    /**
     * The JIRA resource ID.
     */
    private UUID orgId;
}
