package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Objects;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jira.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraProjectResponseDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraRefreshTokenDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraResponseDTO;
import edu.nd.crc.safa.server.entities.api.jira.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.imports.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.jira.JiraConnectionService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraController extends BaseController {

    private final Logger log = LoggerFactory.getLogger(JiraController.class);

    private final JiraAccessCredentialsRepository accessCredentialsRepository;

    private final AppEntityRetrievalService appEntityRetrievalService;
    private final ProjectService projectService;
    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;

    private final ExecutorDelegate executorDelegate;

    @Autowired
    public JiraController(ResourceBuilder resourceBuilder,
                          AppEntityRetrievalService appEntityRetrievalService,
                          ProjectService projectService,
                          SafaUserService safaUserService,
                          JiraAccessCredentialsRepository accessCredentialsRepository,
                          JiraConnectionService jiraConnectionService,
                          ExecutorDelegate executorDelegate) {
        super(resourceBuilder);
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.projectService = projectService;
        this.safaUserService = safaUserService;
        this.accessCredentialsRepository = accessCredentialsRepository;
        this.jiraConnectionService = jiraConnectionService;
        this.executorDelegate = executorDelegate;
    }

    @PostMapping(AppRoutes.Projects.Import.pullJiraProject)
    public DeferredResult<JiraResponseDTO<ProjectEntities>> pullJiraProject(@PathVariable("id") @NotNull Long id,
                                                           @PathVariable("cloudId") String cloudId) {
        DeferredResult<JiraResponseDTO<ProjectEntities>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = accessCredentialsRepository
                .findByUserAndCloudId(principal, cloudId).orElseThrow(() -> new SafaError("No JIRA credentials found"));
            JiraProjectResponseDTO response = jiraConnectionService.retrieveJIRAProject(credentials, id);
            Project project = new Project();

            // Should probably also specify this is a JIRA pulled project
            // Maybe save the cloud id and JIRA project id, so we can later update it?
            project.setName(response.getKey());
            project.setDescription(response.getDescription());
            this.projectService.saveProjectWithCurrentUserAsOwner(project);

            ProjectVersion projectVersion = this.projectService.createBaseProjectVersion(project);
            ProjectEntities projectEntities = appEntityRetrievalService
                .retrieveProjectEntitiesAtProjectVersion(projectVersion);

            output.setResult(new JiraResponseDTO<>(projectEntities, JiraResponseMessage.IMPORTED));
        });

        return output;
    }

    @PostMapping(AppRoutes.Accounts.jiraCredentials)
    public DeferredResult<JiraResponseDTO<Void>> createCredentials(@RequestBody @Valid JiraAccessCredentialsDTO data) {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = data.toEntity();

            boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

            if (!areCredentialsValid) {
                throw new SafaError("Invalid credentials");
            }

            JiraAccessCredentials previousCredentials =
                accessCredentialsRepository.findByUserAndCloudId(principal, credentials.getCloudId()).orElse(null);

            if (Objects.nonNull(previousCredentials)) {
                log.info("Deleting previous JIRA credentials for {}", principal.getEmail());
                accessCredentialsRepository.delete(previousCredentials);
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
            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.CREATED));
        });

        return output;
    }

    @PutMapping(AppRoutes.Accounts.jiraCredentialsRefresh)
    public DeferredResult<JiraResponseDTO<Void>> createCredentials(@PathVariable("cloudId") @NotNull String cloudId) {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = accessCredentialsRepository
                .findByUserAndCloudId(principal, cloudId).orElseThrow(() -> new SafaError("No JIRA credentials found"));

            JiraRefreshTokenDTO newCredentials = jiraConnectionService.refreshAccessToken(credentials);

            if (!StringUtils.hasText(newCredentials.getAccessToken())
                || !StringUtils.hasText(newCredentials.getRefreshToken())) {
                throw new SafaError("Invalid credentials");
            }

            credentials.setBearerAccessToken(newCredentials.getAccessToken().getBytes());
            credentials.setRefreshToken(newCredentials.getRefreshToken());
            credentials = accessCredentialsRepository.save(credentials);

            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.UPDATED));
        });

        return output;
    }

    @GetMapping(AppRoutes.Projects.retrieveJIRAProjects)
    public DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> retrieveJIRAProjects(
        @PathVariable("cloudId") String cloudId) {
        DeferredResult<JiraResponseDTO<List<JiraProjectResponseDTO>>> output =
            executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = accessCredentialsRepository
                .findByUserAndCloudId(principal, cloudId).orElseThrow(() -> new SafaError("No JIRA credentials found"));
            List<JiraProjectResponseDTO> response = jiraConnectionService.retrieveJIRAProjectsPreview(credentials);

            output.setResult(new JiraResponseDTO<>(response, JiraResponseMessage.OK));
        });

        return output;
    }

    @PostMapping(AppRoutes.Accounts.jiraCredentialsValidate)
    public DeferredResult<JiraResponseDTO<Boolean>> validateJIRACredentials(
        @RequestBody @Valid JiraAccessCredentialsDTO data) {
        DeferredResult<JiraResponseDTO<Boolean>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            JiraAccessCredentials credentials = data.toEntity();

            try {
                boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

                output.setResult(new JiraResponseDTO<>(areCredentialsValid, JiraResponseMessage.OK));
            } catch (Exception ex) {
                output.setResult(new JiraResponseDTO<>(false, JiraResponseMessage.ERROR));
            }
        });

        return output;
    }
}
