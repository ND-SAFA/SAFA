package edu.nd.crc.safa.server.services.jira;

import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponse;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;

/**
 * Template JIRA operations
 */
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
     * @param credentials The credentials of the user accessing JIRA.
     * @param id          The JIRA project id.
     * @return JIRA API Response
     */
    JiraProjectResponse retrieveJIRAProject(JiraAccessCredentials credentials, Long id);

    /**
     * Get new credentials based on old ones
     *
     * @param credentials The credentials to refresh.
     * @return Refreshed credentials.
     */
    JiraAccessCredentials refreshAccessToken(JiraAccessCredentials credentials);
}
