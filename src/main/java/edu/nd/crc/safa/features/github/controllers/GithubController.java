package edu.nd.crc.safa.features.github.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO.GithubResponseMessage;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectViaGithubBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectViaGithubBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.context.request.async.DeferredResult;

/**
 * Responsible for pulling and syncing GitHub projects with Safa projects.
 */
@Controller
public class GithubController extends BaseController {

    private static final Logger log = LoggerFactory.getLogger(GithubController.class);

    private final SafaUserService safaUserService;
    private final GithubConnectionService githubConnectionService;
    private final GithubAccessCredentialsRepository githubAccessCredentialsRepository;
    private final ExecutorDelegate executorDelegate;

    public GithubController(ResourceBuilder resourceBuilder,
                            SafaUserService safaUserService,
                            GithubConnectionService githubConnectionService,
                            GithubAccessCredentialsRepository githubAccessCredentialsRepository,
                            ExecutorDelegate executorDelegate,
                            ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.safaUserService = safaUserService;
        this.githubConnectionService = githubConnectionService;
        this.githubAccessCredentialsRepository = githubAccessCredentialsRepository;
        this.executorDelegate = executorDelegate;
    }

    @GetMapping(AppRoutes.Github.RETRIEVE_GITHUB_REPOSITORIES)
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

    @PostMapping(AppRoutes.Github.Import.BY_NAME)
    public DeferredResult<GithubResponseDTO<JobAppEntity>> pullGithubProject(
        @PathVariable("repositoryName") String repositoryName) {
        DeferredResult<GithubResponseDTO<JobAppEntity>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            GithubIdentifier identifier = new GithubIdentifier(null, repositoryName);
            CreateProjectViaGithubBuilder builder = new CreateProjectViaGithubBuilder(serviceProvider, identifier);
            GithubResponseDTO<JobAppEntity> responseDTO = new GithubResponseDTO<>(builder.perform(),
                GithubResponseMessage.OK);

            output.setResult(responseDTO);
        });

        return output;
    }

    @PutMapping(AppRoutes.Github.Import.UPDATE)
    public DeferredResult<GithubResponseDTO<JobAppEntity>> updateGithubProject(
        @PathVariable("versionId") UUID versionId,
        @PathVariable("repositoryName") String repositoryName) {
        DeferredResult<GithubResponseDTO<JobAppEntity>> output = executorDelegate.createOutput(5000L);

        executorDelegate.submit(output, () -> {
            ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
            GithubIdentifier identifier = new GithubIdentifier(projectVersion, repositoryName);
            UpdateProjectViaGithubBuilder builder = new UpdateProjectViaGithubBuilder(serviceProvider, identifier);
            GithubResponseDTO<JobAppEntity> responseDTO = new GithubResponseDTO<>(builder.perform(),
                GithubResponseMessage.OK);

            output.setResult(responseDTO);
        });

        return output;
    }

}
