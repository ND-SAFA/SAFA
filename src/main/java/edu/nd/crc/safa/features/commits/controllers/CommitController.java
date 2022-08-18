package edu.nd.crc.safa.features.commits.controllers;

import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for commit a versioned change to a project's entities.
 */
@RestController
public class CommitController extends BaseController {

    @Autowired
    public CommitController(ResourceBuilder resourceBuilder,
                            ServiceProvider serviceProvider
    ) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Saves given entities to specified project version.
     *
     * @param versionId     The id of the version to commit to.
     * @param projectCommit The entities to commit.
     * @return ProjectCommit The commit containing the entities with any processing additions.
     * @throws SafaError Throws error if user does not have edit permissions on project.
     */
    @PostMapping(AppRoutes.Commits.COMMIT_CHANGE)
    public ProjectCommit commitChange(@PathVariable UUID versionId,
                                      @RequestBody ProjectCommit projectCommit) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        projectCommit.setCommitVersion(projectVersion);
        projectCommit.setFailOnError(true);
        ProjectChanger projectChanger = new ProjectChanger(projectVersion, serviceProvider);
        return projectChanger.commit(projectCommit);
    }
}
