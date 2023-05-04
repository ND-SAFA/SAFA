package edu.nd.crc.safa.features.github.controllers;

import java.util.Optional;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.server.controllers.utils.GithubControllerUtils;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.context.request.async.DeferredResult;

/**
 * Responsible for registering GitHub credentials and linking them up with Safa
 */
@Controller
public class GithubCredentialsController extends BaseController {

    private static final Logger log = LoggerFactory.getLogger(GithubCredentialsController.class);

    private final SafaUserService safaUserService;
    private final GithubConnectionService githubConnectionService;
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final ExecutorDelegate executorDelegate;
    private final GithubControllerUtils githubControllerUtils;

    public GithubCredentialsController(ResourceBuilder resourceBuilder,
                                       SafaUserService safaUserService,
                                       GithubConnectionService githubConnectionService,
                                       GithubAccessCredentialsRepository githubAccessCredentialsRepository,
                                       ExecutorDelegate executorDelegate,
                                       ServiceProvider serviceProvider,
                                       GithubControllerUtils githubControllerUtils) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = safaUserService;
        this.githubConnectionService = githubConnectionService;
        this.githubAccessCredentialsRepository = githubAccessCredentialsRepository;
        this.executorDelegate = executorDelegate;
        this.githubControllerUtils = githubControllerUtils;
    }

    @PostMapping(AppRoutes.Github.Credentials.REGISTER)
    public DeferredResult<Void> createCredentials(
        @NotNull @NotEmpty @PathVariable("accessCode") String accessCode) {
        DeferredResult<Void> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            GithubAccessCredentialsDTO dto = githubConnectionService.useAccessCode(accessCode);

            if (dto.isError()) {
                throw new SafaError("%s %s", dto.getError(), dto.getErrorDescription());
            }

            GithubAccessCredentials credentials = dto.toEntity();
            // If credentials are not valid it will throw
            GithubSelfResponseDTO selfResponseDTO = githubConnectionService.getSelf(credentials);
            Optional<GithubAccessCredentials> previousCredentials = githubAccessCredentialsRepository
                .findByUser(principal);

            if (previousCredentials.isPresent()) {
                log.info("Deleting previous GitHub credentials for {}", principal.getEmail());
                githubAccessCredentialsRepository.delete(previousCredentials.get());
            }

            credentials.setGithubHandler(selfResponseDTO.getLogin());
            credentials.setUser(principal);
            githubAccessCredentialsRepository.save(credentials);
        });

        return output;
    }

    @DeleteMapping(AppRoutes.Github.Credentials.DELETE)
    public DeferredResult<Void> deleteCredentials() {
        DeferredResult<Void> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<GithubAccessCredentials> credentials = githubAccessCredentialsRepository
                .findByUser(principal);

            if (credentials.isEmpty()) {
                return;
            }

            githubAccessCredentialsRepository.delete(credentials.get());
        });

        return output;
    }

    @GetMapping(AppRoutes.Github.Credentials.VALID)
    public DeferredResult<Boolean> validCredentials() {
        DeferredResult<Boolean> output = executorDelegate.createOutput(5000L);

        SafaUser principal = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            Optional<GithubAccessCredentials> credentials = githubConnectionService.getGithubCredentials(principal);

            if (credentials.isEmpty()) {
                output.setResult(false);
            } else {
                output.setResult(githubControllerUtils.checkCredentials(credentials.get()));
            }
        });

        return output;
    }

}
