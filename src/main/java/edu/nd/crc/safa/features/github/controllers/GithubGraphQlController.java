package edu.nd.crc.safa.features.github.controllers;

import java.util.List;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.context.request.async.DeferredResult;

@Controller
public class GithubGraphQlController extends BaseController {
    private static final long REQUEST_TIMEOUT = 30000L;

    private final GithubGraphQlService graphQlService;

    public GithubGraphQlController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.graphQlService = serviceProvider.getGithubGraphQlService();
    }

    /**
     * Get all projects the user has access to.
     *
     * @return Accessible projects.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.ROOT)
    public DeferredResult<List<GithubRepositoryDTO>> retrieveGithubRepositories() {
        return makeDeferredRequest(user -> {
            return GithubRepositoryDTO.fromGraphQlResponse(graphQlService.getGithubRepositories(user));
        }, REQUEST_TIMEOUT);
    }

    /**
     * Get a specific repo by owner and name.
     *
     * @param owner The owner of the project.
     * @param repo  The name of the project.
     * @return The repo.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.BY_OWNER_AND_NAME)
    public DeferredResult<GithubRepositoryDTO> retrieveGithubRepository(@PathVariable("owner") String owner,
                                                                        @PathVariable("repositoryName") String repo) {
        return makeDeferredRequest(user -> {
            return GithubRepositoryDTO.fromGraphQlResponse(graphQlService.getGithubRepository(user, owner, repo));
        });
    }

}
