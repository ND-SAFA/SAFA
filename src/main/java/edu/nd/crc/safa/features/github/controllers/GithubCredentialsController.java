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
import edu.nd.crc.safa.features.github.utils.GithubControllerUtils;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.services.SafaUserService;
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
        return makeDeferredRequest(user -> {
            GithubAccessCredentialsDTO dto = githubConnectionService.useAccessCode(accessCode);

            if (dto.isError()) {
                throw new SafaError("%s %s", dto.getError(), dto.getErrorDescription());
            }

            GithubAccessCredentials credentials = dto.toEntity();
            // If credentials are not valid it will throw
            GithubSelfResponseDTO selfResponseDTO = githubConnectionService.getSelf(credentials);
            Optional<GithubAccessCredentials> previousCredentials = githubAccessCredentialsRepository
                .findByUser(user);

            if (previousCredentials.isPresent()) {
                log.info("Deleting previous GitHub credentials for {}", user.getEmail());
                githubAccessCredentialsRepository.delete(previousCredentials.get());
            }

            credentials.setGithubHandler(selfResponseDTO.getLogin());
            credentials.setUser(user);
            githubAccessCredentialsRepository.save(credentials);
        });
    }

    @DeleteMapping(AppRoutes.Github.Credentials.DELETE)
    public void deleteCredentials() {
        Optional<GithubAccessCredentials> credentials = githubAccessCredentialsRepository
            .findByUser(safaUserService.getCurrentUser());
        credentials.ifPresent(githubAccessCredentialsRepository::delete);
    }

    @GetMapping(AppRoutes.Github.Credentials.VALID)
    public Boolean validCredentials() {
        Optional<GithubAccessCredentials> credentials =
            githubConnectionService.getGithubCredentials(safaUserService.getCurrentUser());
        return credentials.filter(githubControllerUtils::checkCredentials).isPresent();
    }

}
