package edu.nd.crc.safa.features.jobs.entities.app;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.EntityVersionService;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public class ProjectCreationJob extends AbstractJob {
    /**
     * The project version of the
     */
    ProjectCommit projectCommit;
    /**
     * The entities created during job.
     */
    ProjectAppEntity projectAppEntity;
    /**
     * The service used for creating entities.
     */
    EntityVersionService entityVersionService;

    public ProjectCreationJob(JobDbEntity jobDbEntity,
                              ServiceProvider serviceProvider,
                              ProjectCommit projectCommit) {
        super(jobDbEntity, serviceProvider);
        this.projectCommit = projectCommit;
        this.entityVersionService = serviceProvider.getEntityVersionService();
    }

    public void savingArtifacts() throws SafaError {
        this.entityVersionService.setArtifactsAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getArtifacts().getAdded());
    }

    public void savingTraces() throws SafaError {
        this.entityVersionService.setTracesAtVersionAndSaveErrors(
            projectCommit.getCommitVersion(),
            projectCommit.getTraces().getAdded());
    }

    public void generatingLayout() {
        //TODO: Store generated layout
    }

    @Override
    public void done() {
        AppEntityRetrievalService appEntityRetrievalService = serviceProvider.getAppEntityRetrievalService();
        this.projectAppEntity = appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(
            projectCommit.getCommitVersion()
        );
        this.jobDbEntity.setCompletedEntityId(projectCommit.getCommitVersion().getVersionId());
        super.done();
    }
}
