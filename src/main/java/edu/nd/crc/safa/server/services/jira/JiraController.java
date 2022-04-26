package edu.nd.crc.safa.server.services.jira;


import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.controllers.BaseController;
import edu.nd.crc.safa.server.services.jira.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.services.jira.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.jira.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.jira.JiraConnectionServiceImpl;
import edu.nd.crc.safa.server.services.jira.JiraProjectResponse;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraController extends BaseController {

	@Autowired
	private AppEntityRetrievalService appEntityRetrievalService;

	@Autowired
	private ProjectService projectService;

	@Autowired
	private SafaUserService safaUserService;

	@Autowired
	private JiraAccessCredentialsRepository accessCredentialsRepository;

	@Autowired
	private JiraConnectionService jiraConnectionService;

	@Autowired
	private ExecutorDelegate executorDelegate;

	@Autowired
	public JiraController(ResourceBuilder resourceBuilder) {
		super(resourceBuilder);
	}

	@PostMapping(AppRoutes.Projects.Import.pullJiraProject)
	public DeferredResult<ProjectEntities> pullJiraProject(@PathVariable("id") Long id) {
		DeferredResult<ProjectEntities> output = executorDelegate.createOutput(5000L);
		SafaUser principal = safaUserService.getCurrentUser();

		executorDelegate.submit(output, () -> {
			JiraAccessCredentials credentials = accessCredentialsRepository.findByUser(principal).orElseThrow(() -> new SafaError("No JIRA credentials found"));
			JiraProjectResponse response = jiraConnectionService.retrieveJIRAProject(credentials, id);
			Project project = new Project();

			project.setName(response.getKey());
			project.setDescription(response.getDescription());
			this.projectService.saveProjectWithCurrentUserAsOwner(project);

			ProjectVersion projectVersion = this.projectService.createBaseProjectVersion(project);
			ProjectEntities projectEntities = appEntityRetrievalService.retrieveProjectEntitiesAtProjectVersion(projectVersion);

			output.setResult(projectEntities);
		});

		return output;
	}

	@PostMapping(AppRoutes.Accounts.jiraCredentials)
	public DeferredResult<String> createCredentials(@RequestBody @Valid JiraAccessCredentialsDTO data) {
		DeferredResult<String> output = executorDelegate.createOutput(5000L);
		SafaUser principal = safaUserService.getCurrentUser();

		executorDelegate.submit(output, () -> {
			JiraAccessCredentials credentials = data.toEntity();

			boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

			if (!areCredentialsValid) {
				throw new SafaError("Invalid credentials");
			}

			credentials.setUser(principal);
			credentials = accessCredentialsRepository.save(credentials);
			// TODO: Use appropriate messages and a standard object output payload for API responses
			// Payload to be something like
			/*
				{
					payload: <returned-object>
					isError: <true/false>
					status: <HttpCode>
					message: <SafaMessage.EnumConstant>
			 */
			output.setResult("created");
		});

		return output;
	}

}
