package edu.nd.crc.safa.features.jira.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectViaJiraBuilder;
import edu.nd.crc.safa.features.jobs.builders.ImportIntoProjectViaJiraBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectViaJiraBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
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

    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;
    private final ExecutorDelegate executorDelegate;

    @Autowired
    public JiraController(ResourceBuilder resourceBuilder,
                          ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
    }

    @GetMapping(AppRoutes.Jira.Import.RETRIEVE_JIRA_PROJECTS)
    public DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> retrieveJIRAProjects() {
        DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> output =
            executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

            if (credentialsOptional.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            List<JiraInstallationDTO> installations = jiraConnectionService.getInstallations(credentialsOptional.get());

            List<JiraProjectResponseDTO> response = new ArrayList<>();

            for (JiraInstallationDTO installation : installations) {
                response.addAll(jiraConnectionService
                    .retrieveJIRAProjectsPreview(credentialsOptional.get(), installation.getId()));
            }

            output.setResult(new JiraResponseDTO<>(response, JiraResponseMessage.OK));
        });

        return output;
    }

    @PostMapping(AppRoutes.Jira.Import.BY_ID)
    public JiraResponseDTO<JobAppEntity> createJiraProject(@PathVariable("id") Long jiraProjectId,
        @PathVariable String cloudId) throws Exception {

        SafaUser principal = safaUserService.getCurrentUser();
        Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

        if (credentialsOptional.isEmpty()) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED);
        }

        JiraAccessCredentials jiraAccessCredentials = credentialsOptional.get();

        if (!jiraConnectionService.checkUserCanViewProjectIssues(jiraAccessCredentials, cloudId, jiraProjectId)) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.CANNOT_PARSE_PROJECT);
        }

        // version created in job
        CreateProjectViaJiraBuilder createProjectViaJira = new CreateProjectViaJiraBuilder(
            serviceProvider,
            new JiraIdentifier(null, jiraProjectId, cloudId),
            principal);

        return new JiraResponseDTO<>(createProjectViaJira.perform(), JiraResponseMessage.OK);
    }

    @PutMapping(AppRoutes.Jira.Import.UPDATE)
    public JiraResponseDTO<JobAppEntity> updateJiraProject(@PathVariable UUID versionId,
                                                           @PathVariable String cloudId,
                                                           @PathVariable("id") Long jiraProjectId) throws Exception {
        SafaUser principal = safaUserService.getCurrentUser();

        Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

        if (credentialsOptional.isEmpty()) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED);
        }

        JiraAccessCredentials jiraAccessCredentials = credentialsOptional.get();

        if (!jiraConnectionService.checkUserCanViewProjectIssues(jiraAccessCredentials, cloudId, jiraProjectId)) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.CANNOT_PARSE_PROJECT);
        }

        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        JiraIdentifier jiraIdentifier = new JiraIdentifier(projectVersion, jiraProjectId, cloudId);
        UpdateProjectViaJiraBuilder updateProjectViaJira = new UpdateProjectViaJiraBuilder(
            this.serviceProvider,
            jiraIdentifier,
            principal
        );

        return new JiraResponseDTO<>(updateProjectViaJira.perform(), JiraResponseMessage.OK);
    }

    @PostMapping(AppRoutes.Jira.Import.IMPORT_INTO_EXISTING)
    public JiraResponseDTO<JobAppEntity> importIntoExisting(
        @PathVariable UUID versionId,
        @PathVariable String cloudId,
        @PathVariable("id") Long jiraProjectId) throws Exception {

        SafaUser principal = safaUserService.getCurrentUser();

        Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

        if (credentialsOptional.isEmpty()) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED);
        }

        JiraAccessCredentials jiraAccessCredentials = credentialsOptional.get();

        if (!jiraConnectionService.checkUserCanViewProjectIssues(jiraAccessCredentials, cloudId, jiraProjectId)) {
            return new JiraResponseDTO<>(null, JiraResponseMessage.CANNOT_PARSE_PROJECT);
        }

        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        JiraIdentifier jiraIdentifier = new JiraIdentifier(projectVersion, jiraProjectId, cloudId);
        ImportIntoProjectViaJiraBuilder updateProjectViaJira = new ImportIntoProjectViaJiraBuilder(
            this.serviceProvider,
            jiraIdentifier,
            principal
        );

        return new JiraResponseDTO<>(updateProjectViaJira.perform(), JiraResponseMessage.OK);
    }
}
