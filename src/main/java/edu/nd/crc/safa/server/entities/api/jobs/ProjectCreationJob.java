package edu.nd.crc.safa.server.entities.api.jobs;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

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
