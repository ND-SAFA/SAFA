package edu.nd.crc.safa.features.jira.entities.app;

import java.util.List;

import lombok.Data;

/**
 * DTO encapsulating data retrieved when fetching JIRA issues
 *
 */
@Data
public class JiraIssuesResponseDTO {

    List<JiraIssueDTO> issues;
}
