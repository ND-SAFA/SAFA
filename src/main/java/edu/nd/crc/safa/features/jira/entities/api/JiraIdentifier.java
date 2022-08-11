package edu.nd.crc.safa.features.jira.entities.api;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Information for identifying jira project.
 */
@Data
@AllArgsConstructor
public class JiraIdentifier {
    Long jiraProjectId;
    String cloudId;
}
