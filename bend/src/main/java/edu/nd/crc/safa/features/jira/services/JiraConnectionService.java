package edu.nd.crc.safa.features.jira.services;

import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.jira.entities.app.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraAuthResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.context.annotation.Scope;

/**
 * Template JIRA operations
 */
@Scope("singleton")
public interface JiraConnectionService {

    /**
     * Gets access credentials for the given user.
     *
     * @param user The safa user to look up credentials for
     * @return The user's jira credentials, if they exist
     */
    Optional<JiraAccessCredentials> getJiraCredentials(SafaUser user);

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
     * @param orgId         The ID of the resource the project is in.
     * @param jiraProjectId The JIRA project id.
     * @return JIRA API Response
     */
    JiraProjectResponseDTO retrieveJIRAProject(JiraAccessCredentials credentials, UUID orgId, Long jiraProjectId);

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
     * @param orgId       The ID of the resource the projects are in.
     * @return JIRA API Response
     */
    List<JiraProjectResponseDTO> retrieveJIRAProjectsPreview(JiraAccessCredentials credentials, UUID orgId);

    /**
     * Retrieve issues associated with a JIRA project
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param orgId         The ID of the resource the project is in.
     * @param jiraProjectId The JIRA project id.
     * @return JIRA issues for the given project
     */
    List<JiraIssueDTO> retrieveJIRAIssues(JiraAccessCredentials credentials, UUID orgId, Long jiraProjectId);

    /**
     * Retrieve updated issues associated with a JIRA project after a certain timestamp
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param orgId         The ID of the resource the project is in.
     * @param jiraProjectId The JIRA project id.
     * @param timestamp     Timestamp after which issues were updated
     * @return JIRA the updated issues for the given project
     */
    List<JiraIssueDTO> retrieveUpdatedJIRAIssues(JiraAccessCredentials credentials,
                                                 UUID orgId,
                                                 Long jiraProjectId,
                                                 Date timestamp);

    /**
     * Check whether the 'ADMINISTER_PROJECTS' permissions is set for a given user and project id.
     *
     * @param credentials   The credentials of the user accessing JIRA.
     * @param orgId         The ID of the resource the project is in.
     * @param jiraProjectId The JIRA project id.
     * @return A flag indicating the permission existence.
     */
    boolean checkUserCanViewProjectIssues(JiraAccessCredentials credentials, UUID orgId, Long jiraProjectId);

    /**
     * @param accessCode Code retrieved from FEND after user has authorized our application
     * @return Set of JIRA credentials that will be saved for later use.
     */
    JiraAccessCredentialsDTO useAccessCode(String accessCode);

    List<JiraInstallationDTO> getInstallations(JiraAccessCredentials credentials);
}
