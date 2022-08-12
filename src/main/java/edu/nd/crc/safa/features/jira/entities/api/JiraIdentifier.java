package edu.nd.crc.safa.features.jira.entities.api;

import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Information for identifying jira project.
 */
@Data
@AllArgsConstructor
public class JiraIdentifier {
    ProjectVersion projectVersion;
    Long jiraProjectId;
    String cloudId;
}
