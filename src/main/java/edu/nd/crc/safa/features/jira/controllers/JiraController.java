package edu.nd.crc.safa.features.jira.controllers;

import java.util.Date;
import java.util.List;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.repositories.JiraProjectRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.builders.UpdateProjectByJiraJobBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraController extends BaseController {

    private final JiraAccessCredentialsRepository accessCredentialsRepository;
    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;
    private final ExecutorDelegate executorDelegate;
    private final JiraProjectRepository jiraProjectRepository;

    @Autowired
    public JiraController(ResourceBuilder resourceBuilder,
                          ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.accessCredentialsRepository = serviceProvider.getJiraAccessCredentialsRepository();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
        this.jiraProjectRepository = serviceProvider.getJiraProjectRepository();
    }

    @GetMapping(AppRoutes.Jira.RETRIEVE_JIRA_PROJECTS)
    public DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> retrieveJIRAProjects(
        @PathVariable("cloudId") String cloudId) {
        DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> output =
            executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials jiraAccessCredentials = accessCredentialsRepository
                .findByUserAndCloudId(principal, cloudId).orElseThrow(() -> new SafaError("No JIRA credentials found"));
            List<JiraProjectResponseDTO> response = jiraConnectionService
                .retrieveJIRAProjectsPreview(jiraAccessCredentials);

            output.setResult(new JiraResponseDTO<>(response, JiraResponseMessage.OK));
        });

        return output;
    }

    @PostMapping(AppRoutes.Jira.Import.BY_ID)
    public JobAppEntity pullJiraProject(@PathVariable("id") Long jiraProjectId,
                                        @PathVariable("cloudId") String cloudId) throws Exception {

        UpdateProjectByJiraJobBuilder updateProjectByJiraJobBuilder = new UpdateProjectByJiraJobBuilder(
            serviceProvider,
            jiraProjectId,
            cloudId);
        return updateProjectByJiraJobBuilder.perform();
    }

    @PutMapping(AppRoutes.Jira.Import.BY_ID)
    // TODO: Modify the output of the endpoint. Currently it retrieves the updated issues for testing purposes
    public DeferredResult<JiraIssuesResponseDTO> updateJiraProject(@PathVariable("id") Long jiraProjectId,
                                                                   @PathVariable("cloudId") String cloudId) {
        DeferredResult<JiraIssuesResponseDTO> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            // TODO: @Alberto, please update the artifacts given the changed issues
            JiraProject jiraProject = jiraProjectRepository.findByJiraProjectId(jiraProjectId)
                .orElseThrow(() -> new SafaError("JIRA project not imported"));
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = accessCredentialsRepository
                .findByUserAndCloudId(principal, cloudId).orElseThrow(() -> new SafaError("No JIRA credentials found"));
            JiraIssuesResponseDTO dto = jiraConnectionService.retrieveUpdatedJIRAIssues(credentials, jiraProjectId,
                jiraProject.getLastUpdate());

            jiraProject.setLastUpdate(new Date());
            jiraProjectRepository.save(jiraProject);
            output.setResult(dto);
        });

        return output;
    }
}
