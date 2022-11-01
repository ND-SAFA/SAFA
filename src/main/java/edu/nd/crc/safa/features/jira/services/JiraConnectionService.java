package edu.nd.crc.safa.features.jira.services;

import java.util.Date;
import java.util.List;

import edu.nd.crc.safa.features.jira.entities.app.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraAuthResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;

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
    JiraAuthResponseDTO refreshAccessToken(JiraAccessCredentials credentials);

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
     * @return JiraProject The jira project created.
     */
    JiraProject createJiraProjectMapping(Project project, Long jiraProjectId);

    /**
     * Retrieve updated issues associated with a JIRA project after a certain timestamp
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param jiraProjectId The JIRA project id.
     * @param timestamp     Timestamp after which issues were updated
     * @return JIRA the updated issues for the given project
     */
    JiraIssuesResponseDTO retrieveUpdatedJIRAIssues(JiraAccessCredentials credentials,
                                                    Long jiraProjectId,
                                                    Date timestamp);

    /**
     * Check whether the 'ADMINISTER_PROJECTS' permissions is set for a given user and project id.
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param jiraProjectId The JIRA project id.
     * @return A flag indicating the permission existence.
     */
    boolean checkUserCanViewProjectIssues(JiraAccessCredentials credentials, Long jiraProjectId);

    /**
     * @param accessCode Code retrieved from FEND after user has authorized our application
     * @return Set of JIRA credentials that will be saved for later use.
     */
    JiraAccessCredentialsDTO useAccessCode(String accessCode);

    List<JiraInstallationDTO> getInstallations(JiraAccessCredentials credentials);
}
