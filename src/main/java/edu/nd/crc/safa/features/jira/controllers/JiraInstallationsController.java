package edu.nd.crc.safa.features.jira.controllers;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.app.JiraInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraResponseDTO.JiraResponseMessage;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling JIRA installations.
 */
@Controller
public class JiraInstallationsController extends BaseController {

    private final Logger log = LoggerFactory.getLogger(JiraInstallationsController.class);
    private final JiraAccessCredentialsRepository accessCredentialsRepository;
    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;
    private final ExecutorDelegate executorDelegate;

    @Autowired
    public JiraInstallationsController(ResourceBuilder resourceBuilder,
                                       ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.accessCredentialsRepository = serviceProvider.getJiraAccessCredentialsRepository();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
    }

    @GetMapping(AppRoutes.Jira.Installations.RETRIEVE_AVAILABLE)
    public DeferredResult<JiraResponseDTO<List<JiraInstallationDTO>>> retrieveAvailableInstallations() {
        DeferredResult<JiraResponseDTO<List<JiraInstallationDTO>>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            Optional<JiraAccessCredentials> credentials = accessCredentialsRepository
                .findByUser(principal);

            if (credentials.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            output.setResult(new JiraResponseDTO<>(jiraConnectionService.getInstallations(credentials.get()),
                JiraResponseMessage.OK));
        });

        return output;
    }

    @PutMapping(AppRoutes.Jira.Installations.REGISTER)
    public DeferredResult<JiraResponseDTO<Void>> registerInstallation(
        @PathVariable("cloudId") String cloudId) {
        DeferredResult<JiraResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            if (!StringUtils.hasText(cloudId)) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.ERROR));
                return;
            }

            SafaUser principal = safaUserService.getCurrentUser();
            Optional<JiraAccessCredentials> credentialsOptional = accessCredentialsRepository
                .findByUser(principal);

            if (credentialsOptional.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            JiraAccessCredentials credentials = credentialsOptional.get();

            credentials.setCloudId(cloudId);

            if (!jiraConnectionService.checkCredentials(credentials)) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.INVALID_CREDENTIALS));
                return;
            }


            accessCredentialsRepository.save(credentials);
            output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.OK));

        });

        return output;
    }
}
