package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Objects;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.server.entities.api.github.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubRefreshTokenDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubRepositoryDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubResponseDTO;
import edu.nd.crc.safa.server.entities.api.github.GithubResponseDTO.GithubResponseMessage;
import edu.nd.crc.safa.server.entities.api.github.GithubSelfResponseDTO;
import edu.nd.crc.safa.server.entities.api.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.server.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.server.repositories.github.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.server.services.github.GithubConnectionService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.context.request.async.DeferredResult;

/**
 * Responsible for pulling and syncing GitHub projects with Safa projects.
 */
@Controller
public class GithubController extends BaseController {

    private final Logger log = LoggerFactory.getLogger(GithubController.class);

    private final SafaUserService safaUserService;
    private final GithubConnectionService githubConnectionService;
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final ExecutorDelegate executorDelegate;
    private final ServiceProvider serviceProvider;

    public GithubController(ResourceBuilder resourceBuilder,
                            SafaUserService safaUserService,
                            GithubConnectionService githubConnectionService,
                            GithubAccessCredentialsRepository githubAccessCredentialsRepository,
                            ExecutorDelegate executorDelegate,
                            ServiceProvider serviceProvider) {
        super(resourceBuilder);
        this.safaUserService = safaUserService;
        this.githubConnectionService = githubConnectionService;
        this.githubAccessCredentialsRepository = githubAccessCredentialsRepository;
        this.executorDelegate = executorDelegate;
        this.serviceProvider = serviceProvider;
    }

    @PostMapping(AppRoutes.Accounts.Github.GITHUB_CREDENTIALS)
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

    @PutMapping(AppRoutes.Accounts.Github.GITHUB_ACCESS_CREDENTIALS_REFRESH)
    public DeferredResult<GithubResponseDTO<Void>> refreshCredentials() {
        DeferredResult<GithubResponseDTO<Void>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            GithubAccessCredentials githubAccessCredentials = githubAccessCredentialsRepository.findByUser(principal)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));

            GithubResponseDTO<Void> responseDTO = this.checkCredentials(githubAccessCredentials);

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

    @GetMapping(AppRoutes.Projects.RETRIEVE_GITHUB_REPOSITORIES)
    public DeferredResult<GithubResponseDTO<List<GithubRepositoryDTO>>> retrieveGithubRepositories() {
        DeferredResult<GithubResponseDTO<List<GithubRepositoryDTO>>> output =
            executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            SafaUser principal = safaUserService.getCurrentUser();
            GithubAccessCredentials githubAccessCredentials = githubAccessCredentialsRepository.findByUser(principal)
                .orElseThrow(() -> new SafaError("No GitHub credentials found"));
            List<GithubRepositoryDTO> githubRepositoryDTOList = githubConnectionService
                .getUserRepositories(githubAccessCredentials);

            output.setResult(new GithubResponseDTO<>(githubRepositoryDTOList, GithubResponseMessage.OK));
        });

        return output;
    }

    @PostMapping(AppRoutes.Projects.Import.PULL_GITHUB_REPOSITORY)
    public DeferredResult<GithubResponseDTO<JobAppEntity>> pullJiraProject(
        @PathVariable("repositoryName") String repositoryName) {
        DeferredResult<GithubResponseDTO<JobAppEntity>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            JobService jobService = this.serviceProvider.getJobService();

            // Step - Create job identifier
            String jobName = GithubProjectCreationJob.createJobName(repositoryName);
            JobDbEntity jobDbEntity = jobService.createNewJob(JobType.GITHUB_PROJECT_CREATION, jobName);

            // Step - Create jira project creation job
            GithubProjectCreationJob job = new GithubProjectCreationJob(jobDbEntity, serviceProvider, repositoryName);

            // Step - Start job
            jobService.executeJob(jobDbEntity, serviceProvider, job);

            // Step - Respond with project
            output.setResult(new GithubResponseDTO<>(JobAppEntity.createFromJob(jobDbEntity),
                GithubResponseMessage.OK));
        });

        return output;
    }

    private <T> GithubResponseDTO<T> checkCredentials(GithubAccessCredentials credentials) {
        if (credentials.areCredentialsExpired()) {
            log.info("Deleting GitHub credentials");
            githubAccessCredentialsRepository.delete(credentials);
            return new GithubResponseDTO<>(null, GithubResponseMessage.EXPIRED);
        }
        if (credentials.isTokenExpired()) {
            return new GithubResponseDTO<>(null, GithubResponseMessage.TOKEN_REFRESH_REQUIRED);
        }

        return new GithubResponseDTO<>(null, GithubResponseMessage.OK);
    }

}
