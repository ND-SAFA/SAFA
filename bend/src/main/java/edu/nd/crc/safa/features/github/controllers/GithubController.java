package edu.nd.crc.safa.features.github.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.github.utils.GithubControllerUtils;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectViaGithubBuilder;
import edu.nd.crc.safa.features.jobs.builders.ImportIntoProjectViaGithubBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectViaGithubBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.stereotype.Controller;
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

    private final GithubConnectionService githubConnectionService;
    private final GithubControllerUtils githubControllerUtils;

    public GithubController(ResourceBuilder resourceBuilder,
                            ServiceProvider serviceProvider,
                            GithubConnectionService githubConnectionService,
                            GithubControllerUtils githubControllerUtils) {
        super(resourceBuilder, serviceProvider);
        this.githubConnectionService = githubConnectionService;
        this.githubControllerUtils = githubControllerUtils;
    }

    /**
     * Creates a job that imports a GitHub repository into a new SAFA project.
     *
     * @param repositoryName The name of the repository to import.
     * @param owner          The owner of the repository to import.
     * @param importSettings The settings for the import. All fields are optional.
     * @return A {@link JobAppEntity} representing the import job.
     */
    @PostMapping(AppRoutes.Github.Import.BY_NAME)
    public DeferredResult<JobAppEntity> pullGithubProject(@PathVariable("repositoryName") String repositoryName,
                                                          @PathVariable("owner") String owner,
                                                          @RequestBody GithubImportDTO importSettings) {

        return makeDeferredRequest(user -> {
            checkCredentials(user);
            GithubIdentifier identifier = new GithubIdentifier(null, owner, repositoryName);
            CreateProjectViaGithubBuilder builder
                = new CreateProjectViaGithubBuilder(getServiceProvider(), identifier, importSettings, user);
            return builder.perform();
        });
    }

    /**
     * Creates a job that re-imports a GitHub repository into a SAFA project after it has
     * already been previously imported.
     *
     * @param repositoryName The name of the repository to import.
     * @param versionId      The ID of the project version to import into.
     * @param owner          The owner of the repository to import.
     * @param importSettings The settings for the import. All fields are optional.
     * @return Information about the started job
     */
    @PutMapping(AppRoutes.Github.Import.UPDATE)
    public DeferredResult<JobAppEntity> updateGithubProject(@PathVariable("versionId") UUID versionId,
                                                            @PathVariable("repositoryName") String repositoryName,
                                                            @PathVariable("owner") String owner,
                                                            @RequestBody GithubImportDTO importSettings) {
        return makeDeferredRequest(user -> {
            checkCredentials(user);
            ProjectVersion projectVersion = getResourceBuilder()
                .fetchVersion(versionId)
                .withPermission(ProjectPermission.EDIT_DATA, user)
                .withPermission(ProjectPermission.EDIT_INTEGRATIONS, user)
                .get();
            GithubIdentifier identifier = new GithubIdentifier(projectVersion, owner, repositoryName);
            UpdateProjectViaGithubBuilder builder
                = new UpdateProjectViaGithubBuilder(getServiceProvider(), identifier, importSettings, user);
            return builder.perform();
        });
    }

    /**
     * Creates a job that imports a GitHub repository into an existing SAFA project that has
     * not previously had that repository imported into it.
     *
     * @param repositoryName The name of the repository to import.
     * @param versionId      The ID of the project version to import into.
     * @param owner          The owner of the repository to import.
     * @param importSettings The settings for the import. All fields are optional.
     * @return Information about the started job
     */
    @PostMapping(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
    public DeferredResult<JobAppEntity> importIntoExistingProject(@PathVariable("versionId") UUID versionId,
                                                                  @PathVariable("repositoryName") String repositoryName,
                                                                  @PathVariable("owner") String owner,
                                                                  @RequestBody GithubImportDTO importSettings) {
        return makeDeferredRequest(user -> {
            checkCredentials(user);
            ProjectVersion projectVersion = getResourceBuilder()
                .fetchVersion(versionId)
                .withPermission(ProjectPermission.EDIT_DATA, user)
                .withPermission(ProjectPermission.EDIT_INTEGRATIONS, user)
                .get();
            GithubIdentifier identifier = new GithubIdentifier(projectVersion, owner, repositoryName);
            ImportIntoProjectViaGithubBuilder builder
                = new ImportIntoProjectViaGithubBuilder(getServiceProvider(), identifier, importSettings, user);
            return builder.perform();
        });
    }

    private void checkCredentials(SafaUser user) {
        GithubAccessCredentials githubAccessCredentials = githubConnectionService.getGithubCredentials(user)
            .orElseThrow(() -> new SafaError("No GitHub credentials found"));

        boolean response = githubControllerUtils.checkCredentials(githubAccessCredentials);

        if (!response) {
            throw new SafaError("Invalid GitHub credentials");
        }
    }

}
