package edu.nd.crc.safa.features.jira.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectViaJiraBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectViaJiraBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
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

    @Autowired
    public JiraController(ResourceBuilder resourceBuilder,
                          ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.accessCredentialsRepository = serviceProvider.getJiraAccessCredentialsRepository();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
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
    public JobAppEntity createJiraProject(@PathVariable("id") Long jiraProjectId,
                                          @PathVariable("cloudId") String cloudId) throws Exception {

        CreateProjectViaJiraBuilder createProjectViaJira = new CreateProjectViaJiraBuilder(
            serviceProvider,
            new JiraIdentifier(null, jiraProjectId, cloudId)); // version created in job
        return createProjectViaJira.perform();
    }

    @PutMapping(AppRoutes.Jira.Import.UPDATE)
    public JobAppEntity updateJiraProject(@PathVariable UUID versionId,
                                          @PathVariable("id") Long jiraProjectId,
                                          @PathVariable("cloudId") String cloudId) throws Exception {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        JiraIdentifier jiraIdentifier = new JiraIdentifier(projectVersion, jiraProjectId, cloudId);
        UpdateProjectViaJiraBuilder updateProjectViaJira = new UpdateProjectViaJiraBuilder(
            this.serviceProvider,
            jiraIdentifier
        );
        return updateProjectViaJira.perform();
    }
}
