package edu.nd.crc.safa.server.entities.api.jobs;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public class ProjectCreationWorker extends JobWorker {
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

    public ProjectCreationWorker(JobDbEntity jobDbEntity,
                                 ProjectCommit projectCommit) {
        super(jobDbEntity);
        this.projectCommit = projectCommit;
        this.entityVersionService = EntityVersionService.getInstance();
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
    }

    @Override
    public void done() {
        this.projectAppEntity = AppEntityRetrievalService.getInstance().retrieveProjectEntitiesAtProjectVersion(
            projectCommit.getCommitVersion()
        );
        this.jobDbEntity.setCompletedEntityId(projectCommit.getCommitVersion().getVersionId());
        super.done();
    }
}
