package edu.nd.crc.safa.server.services.jira;

import java.util.Date;
import java.util.List;

import edu.nd.crc.safa.server.entities.api.jira.JiraIssuesResponseDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponseDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraRefreshTokenDTO;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.context.annotation.Scope;

/**
 * Template JIRA operations
 */
@Scope("singleton")
public interface JiraConnectionService {

    /**
     * Validate received credentials
     *
     * @param credentials The credentials to be checked.
     * @return Whether given credentials are valid.
     */
    boolean checkCredentials(JiraAccessCredentials credentials);

    /**
     * Retrieve a JIRA project by its id
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param jiraProjectId The JIRA project id.
     * @return JIRA API Response
     */
    JiraProjectResponseDTO retrieveJIRAProject(JiraAccessCredentials credentials, Long jiraProjectId);

    /**
     * Get new credentials based on old ones
     *
     * @param credentials The credentials to refresh.
     * @return Refreshed credentials.
     */
    JiraRefreshTokenDTO refreshAccessToken(JiraAccessCredentials credentials);

    /**
     * Retrieve all JIRA projects
     *
     * @param credentials The credentials of the user accessing JIRA.
     * @return JIRA API Response
     */
    List<JiraProjectResponseDTO> retrieveJIRAProjectsPreview(JiraAccessCredentials credentials);

    /**
     * Retrieve issues associated with a JIRA project
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param jiraProjectId The JIRA project id.
     * @return JIRA issues for the given project
     */
    JiraIssuesResponseDTO retrieveJIRAIssues(JiraAccessCredentials credentials, Long jiraProjectId);

    /**
     * Creates a mapping between the safa project and the jira project.
     *
     * @param project       The safa project associated with the JIRA project.
     * @param jiraProjectId The id of the JIRA project.
     */
    void createJiraProjectMapping(Project project, Long jiraProjectId);

    /**
     * Retrieve updated issues associated with a JIRA project after a certain timestamp
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param jiraProjectId The JIRA project id.
     * @return JIRA the updated issues for the given project
     */
    JiraIssuesResponseDTO retrieveUpdatedJIRAIssues(JiraAccessCredentials credentials, Long jiraProjectId, Date timestamp);
}
