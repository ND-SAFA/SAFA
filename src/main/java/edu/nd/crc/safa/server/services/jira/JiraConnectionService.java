package edu.nd.crc.safa.server.services.jira;


/**
 * Template JIRA operations
 */
public interface JiraConnectionService {

	/**
	 * Validate received credentials
	 */
	boolean checkCredentials(JiraAccessCredentials credentials);

	/**
	 * Retrieve a JIRA project by its id
	 */
	JiraProjectResponse retrieveJIRAProject(JiraAccessCredentials credentials, Long id);

	/**
	 * Get new credentials based on old ones
	 */
	JiraAccessCredentials refreshAccessToken(JiraAccessCredentials credentials);
}
