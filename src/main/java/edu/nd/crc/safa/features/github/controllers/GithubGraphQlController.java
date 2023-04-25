package edu.nd.crc.safa.features.github.controllers;

import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.utilities.ExecutorDelegate;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.context.request.async.DeferredResult;

@Controller
public class GithubGraphQlController extends BaseController {
    private final ExecutorDelegate executorDelegate;
    private final SafaUserService safaUserService;
    private final GithubGraphQlService graphQlService;

    public GithubGraphQlController(ResourceBuilder resourceBuilder,
                                   ServiceProvider serviceProvider,
                                   ExecutorDelegate executorDelegate) {

        super(resourceBuilder, serviceProvider);
        this.executorDelegate = executorDelegate;

        this.safaUserService = serviceProvider.getSafaUserService();
        this.graphQlService = serviceProvider.getGithubGraphQlService();
    }

    /**
     * Get all projects the user has access to.
     *
     * @return Accessible projects.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.ROOT)
    public DeferredResult<List<GithubRepositoryDTO>> retrieveGithubRepositories() {
        return makeDeferredRequest(user ->
            GithubRepositoryDTO.fromGraphQlResponse(graphQlService.getGithubRepositories(user)));
    }

    /**
     * Get a specific repo by owner and name.
     *
     * @param owner The owner of the project.
     * @param repo The name of the project.
     * @return The repo.
     */
    @GetMapping(AppRoutes.Integrations.Github.Repos.BY_OWNER_AND_NAME)
    public DeferredResult<GithubRepositoryDTO> retrieveGithubRepository(@PathVariable("owner") String owner,
                                                                        @PathVariable("repositoryName") String repo) {
        return makeDeferredRequest(user ->
            GithubRepositoryDTO.fromGraphQlResponse(graphQlService.getGithubRepository(user, owner, repo)));
    }

    /**
     * Perform a deferred request which will make the request in the background.
     *
     * @param request The request to make.
     * @param <T> The desired output type.
     * @return A deferred result that will perform the request.
     */
    private <T> DeferredResult<T> makeDeferredRequest(Function<SafaUser, T> request) {

        DeferredResult<T> output = executorDelegate.createOutput(5000L);

        SafaUser user = safaUserService.getCurrentUser();
        executorDelegate.submit(output, () -> {
            T result = request.apply(user);
            output.setResult(result);
        });

        return output;
    }

}
