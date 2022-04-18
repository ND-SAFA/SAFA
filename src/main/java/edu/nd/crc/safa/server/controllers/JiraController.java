package edu.nd.crc.safa.server.controllers;


import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.JIRAProjectPullRequest;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.jira.JiraProjectResponse;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraController extends BaseController {

	@Autowired
	AppEntityRetrievalService appEntityRetrievalService;

	@Autowired
	ProjectService projectService;

	@Autowired
	SafaUserService safaUserService;

	@Autowired
	JiraAccessCredentialsRepository accessCredentialsRepository;

	@Autowired
	JiraConnectionService jiraConnectionService;

	@Autowired
	public JiraController(ResourceBuilder resourceBuilder) {
		super(resourceBuilder);
	}

	@PostMapping(AppRoutes.Projects.Import.pullJiraProject)
	public ProjectEntities pullJiraProject(@PathVariable("id") Long id) throws SafaError {
		SafaUser principal = safaUserService.getCurrentUser();
		JiraAccessCredentials credentials = accessCredentialsRepository.findByUser(principal)
												.orElseThrow(() -> new SafaError("No JIRA credentials found"));
		JiraProjectResponse response = jiraConnectionService.retrieveJIRAProject(credentials, id);
		Project project = new Project();

		project.setName(response.getKey());
		project.setDescription(response.getDescription());
		this.projectService.saveProjectWithCurrentUserAsOwner(project);

		ProjectVersion projectVersion = this.projectService.createBaseProjectVersion(project);

		return appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);
	}

	@PostMapping(AppRoutes.Accounts.jiraCredentials)
	public String pullJiraProject(@RequestBody JIRAProjectPullRequest data) throws SafaError {
		Project project = new Project();

		SafaUser principal = safaUserService.getCurrentUser();
		JiraAccessCredentials credentials = new JiraAccessCredentials();

		credentials.setBearerAccessToken(data.getBearerAccessToken());
		credentials.setClientSecret(data.getClientSecret());
		credentials.setProjectId(data.getProjectId());
		credentials.setCloudId(data.getCloudId());

		boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

		if (!areCredentialsValid) {
			throw new SafaError("Invalid credentials");
		}

		credentials.setUser(safaUserService.getCurrentUser());
		credentials = accessCredentialsRepository.save(credentials);
		return "created"; // todo: not really sure what to return
	}

}
