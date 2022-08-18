package edu.nd.crc.safa.features.jira.controllers;

import java.util.Objects;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.app.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraRefreshTokenDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling and syncing JIRA projects with Safa projects.
 */
@Controller
public class JiraCredentialsController extends BaseController {

    private final Logger log = LoggerFactory.getLogger(JiraCredentialsController.class);
    private final JiraAccessCredentialsRepository accessCredentialsRepository;
    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;
    private final ExecutorDelegate executorDelegate;

    @Autowired
    public JiraCredentialsController(ResourceBuilder resourceBuilder,
                                     ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.accessCredentialsRepository = serviceProvider.getJiraAccessCredentialsRepository();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
    }

    @PostMapping(AppRoutes.Jira.Credentials.ROOT)
    public DeferredResult<JiraResponseDTO<Void>> createCredentials(@RequestBody @Valid JiraAccessCredentialsDTO data) {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            JiraAccessCredentials credentials = data.toEntity();

            boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

            if (!areCredentialsValid) {
                throw new SafaError("User contains invalid JIRA credentials.");
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

    @PutMapping(AppRoutes.Jira.Credentials.REFRESH)
    public DeferredResult<JiraResponseDTO<Void>> createCredentials(@PathVariable("cloudId") String cloudId) {
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

    @PostMapping(AppRoutes.Jira.Credentials.VALIDATE)
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
