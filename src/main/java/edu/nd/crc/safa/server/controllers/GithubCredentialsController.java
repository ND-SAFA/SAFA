package edu.nd.crc.safa.server.controllers;

import java.util.Objects;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubRefreshTokenDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO.GithubResponseMessage;
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
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
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

    @PostMapping(AppRoutes.Github.Credentials.ROOT)
    public DeferredResult<GithubResponseDTO<Void>> createCredentials(
        @RequestBody @Valid GithubAccessCredentialsDTO data) {
        DeferredResult<GithubResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            GithubAccessCredentials credentials = data.toEntity();
            // If credentials are not valid it will throw
            GithubSelfResponseDTO selfResponseDTO = githubConnectionService.getSelf(credentials);
            GithubAccessCredentials previousCredentials = githubAccessCredentialsRepository
                .findByUser(principal).orElse(null);

            if (Objects.nonNull(previousCredentials)) {
                log.info("Deleting previous GitHub credentials for {}", principal.getEmail());
                githubAccessCredentialsRepository.delete(previousCredentials);
            }

            credentials.setGithubHandler(selfResponseDTO.getLogin());
            credentials.setUser(principal);
            githubAccessCredentialsRepository.save(credentials);

            output.setResult(new GithubResponseDTO<>(null, GithubResponseMessage.CREATED));
        });

        return output;
    }

    @PutMapping(AppRoutes.Github.Credentials.REFRESH)
    public DeferredResult<GithubResponseDTO<Void>> refreshCredentials() {
        DeferredResult<GithubResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            GithubAccessCredentials githubAccessCredentials = githubAccessCredentialsRepository.findByUser(principal)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));

            GithubResponseDTO<Void> responseDTO = githubControllerUtils.checkCredentials(githubAccessCredentials);

            if (GithubResponseMessage.EXPIRED.equals(responseDTO.getMessage())) {
                log.error("Trying to refresh expired credentials");
                githubAccessCredentialsRepository.delete(githubAccessCredentials);
                output.setErrorResult(responseDTO);
                return;
            }

            log.info("Refreshing GitHub credentials for {}", principal.getEmail());

            GithubRefreshTokenDTO refreshTokenDTO = githubConnectionService.refreshAccessToken(githubAccessCredentials);

            githubAccessCredentials.setAccessToken(refreshTokenDTO.getAccessToken());
            githubAccessCredentials.setRefreshToken(refreshTokenDTO.getRefreshToken());
            githubAccessCredentials.setAccessTokenExpiration(refreshTokenDTO.getAccessTokenExpiration());
            githubAccessCredentials.setRefreshTokenExpiration(refreshTokenDTO.getRefreshTokenExpiration());
            githubAccessCredentialsRepository.save(githubAccessCredentials);

            output.setResult(new GithubResponseDTO<>(null, GithubResponseMessage.UPDATED));
        });

        return output;
    }
}
