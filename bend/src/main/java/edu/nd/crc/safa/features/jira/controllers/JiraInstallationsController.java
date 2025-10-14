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
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.context.request.async.DeferredResult;


/**
 * Responsible for pulling JIRA installations.
 */
@Controller
public class JiraInstallationsController extends BaseController {

    private final Logger log = LoggerFactory.getLogger(JiraInstallationsController.class);
    private final SafaUserService safaUserService;
    private final JiraConnectionService jiraConnectionService;
    private final ExecutorDelegate executorDelegate;

    @Autowired
    public JiraInstallationsController(ResourceBuilder resourceBuilder,
                                       ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = serviceProvider.getSafaUserService();
        this.jiraConnectionService = serviceProvider.getJiraConnectionService();
        this.executorDelegate = serviceProvider.getExecutorDelegate();
    }

    @GetMapping(AppRoutes.Jira.Installations.RETRIEVE_AVAILABLE)
    public DeferredResult<JiraResponseDTO<List<JiraInstallationDTO>>> retrieveAvailableInstallations() {
        DeferredResult<JiraResponseDTO<List<JiraInstallationDTO>>> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<JiraAccessCredentials> credentials = jiraConnectionService.getJiraCredentials(principal);

            if (credentials.isEmpty()) {
                output.setResult(new JiraResponseDTO<>(null, JiraResponseMessage.NO_CREDENTIALS_REGISTERED));
                return;
            }

            output.setResult(new JiraResponseDTO<>(jiraConnectionService.getInstallations(credentials.get()),
                JiraResponseMessage.OK));
        });

        return output;
    }
}
