package edu.nd.crc.safa.features.jira.controllers;

import java.util.Objects;
import java.util.Optional;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.app.JiraAccessCredentialsDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraAuthResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
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

    @PostMapping(AppRoutes.Jira.Credentials.REGISTER)
    public DeferredResult<JiraResponseDTO<Void>> registerCredentials(
        @NotNull @NotEmpty @PathVariable("accessCode") String accessCode) {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            JiraAccessCredentialsDTO data = jiraConnectionService.useAccessCode(accessCode);
            JiraAccessCredentials credentials = data.toEntity();
            JiraAccessCredentials previousCredentials =
                accessCredentialsRepository.findByUser(principal).orElse(null);

            if (Objects.nonNull(previousCredentials)) {
                log.info("Deleting previous JIRA credentials for {}", principal.getEmail());
                accessCredentialsRepository.delete(previousCredentials);
            }

            credentials.setUser(principal);
            credentials = accessCredentialsRepository.save(credentials);
            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.CREATED));
        });

        return output;
    }

    @PutMapping(AppRoutes.Jira.Credentials.REFRESH)
    public DeferredResult<JiraResponseDTO<Void>> createCredentials() {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

            if (credentialsOptional.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            JiraAccessCredentials credentials = credentialsOptional.get();
            JiraAuthResponseDTO newCredentials = jiraConnectionService.refreshAccessToken(credentials);

            if (!StringUtils.hasText(newCredentials.getAccessToken())
                || !StringUtils.hasText(newCredentials.getRefreshToken())) {
                throw new SafaError("Invalid credentials");
            }

            credentials.setBearerAccessToken(newCredentials.getAccessToken().getBytes());
            credentials.setRefreshToken(newCredentials.getRefreshToken());
            accessCredentialsRepository.save(credentials);

            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.UPDATED));
        });

        return output;
    }

    @GetMapping(AppRoutes.Jira.Credentials.VALIDATE)
    public DeferredResult<JiraResponseDTO<Boolean>> validateJIRACredentials() {
        DeferredResult<JiraResponseDTO<Boolean>> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<JiraAccessCredentials> credentialsOptional = jiraConnectionService.getJiraCredentials(principal);

            if (credentialsOptional.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            JiraAccessCredentials credentials = credentialsOptional.get();

            try {
                boolean areCredentialsValid = jiraConnectionService.checkCredentials(credentials);

                output.setResult(new JiraResponseDTO<>(areCredentialsValid, JiraResponseMessage.OK));
            } catch (Exception ex) {
                output.setResult(new JiraResponseDTO<>(false, JiraResponseMessage.ERROR));
            }
        });

        return output;
    }

    @DeleteMapping(AppRoutes.Jira.Credentials.REFRESH)
    public DeferredResult<JiraResponseDTO<Void>> deleteCredentials() {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<JiraAccessCredentials> credentialsOptional = accessCredentialsRepository
                .findByUser(principal);

            if (credentialsOptional.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            accessCredentialsRepository.delete(credentialsOptional.get());
            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.OK));
        });

        return output;
    }
}
