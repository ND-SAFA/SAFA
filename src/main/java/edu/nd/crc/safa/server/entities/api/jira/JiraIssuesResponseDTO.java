package edu.nd.crc.safa.server.entities.api.jira;

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
