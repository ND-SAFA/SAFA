package edu.nd.crc.safa.server.entities.api.jobs;

import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

public class ProjectCreationWorker extends JobWorker {
    /**
     * The project version of the
     */
    ProjectCommit projectCommit;

    /**
     * The entities created during job.
     */
    ProjectEntities projectEntities;

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
    protected void onComplete() {
        super.onComplete();
        this.projectEntities = AppEntityRetrievalService.getInstance().retrieveProjectEntitiesAtProjectVersion(
            projectCommit.getCommitVersion()
        );
    }
}
